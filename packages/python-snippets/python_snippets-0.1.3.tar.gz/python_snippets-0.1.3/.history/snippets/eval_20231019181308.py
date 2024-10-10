#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/19 18:13:06
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from typing import List, Dict, Set, Sequence, Any
import time
import requests
from snippets import *
# from views.common import request_chatbot
# from snippets import load_lines, batch_process
import logging
import click
logger = logging.getLogger(__name__)


# 计算f1


def get_f1(precision, recall):
    f1 = 0. if precision + recall == 0 else 2 * \
        precision * recall / (precision + recall)
    return f1


# 获得precision和recall值
def get_pr(tp, fp, fn):
    precision = 0. if tp + fp == 0 else tp / (tp + fp)
    recall = 0. if tp + fn == 0 else tp / (tp + fn)
    return dict(precision=precision, recall=recall)


# 获得tp,fp,fn集合
def get_tp_fp_fn_set(true_set, pred_set):
    tp_set = true_set & pred_set
    fp_set = pred_set - tp_set
    fn_set = true_set - tp_set
    return tp_set, fp_set, fn_set


# 测评两个集合
def eval_sets(true_set, pred_set):
    tp_set, fp_set, fn_set = get_tp_fp_fn_set(true_set, pred_set)
    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)
    rs_dict = dict(tp=tp, fp=fp, fn=fn)
    pr_dict = get_pr(tp, fp, fn)
    rs_dict.update(**pr_dict)
    rs_dict.update(f1=get_f1(rs_dict['precision'], rs_dict['recall']))

    return rs_dict


def gen_with_job_id(job_id, url, start, detail=False, timeout=30, interval=0.0):
    url = url+"/get_resp"
    req = dict(job_id=job_id)
    content = ""
    first_token_cost = 0
    total_words = 0
    total_cost = 0

    while True:
        resp = requests.post(url=url, json=req)
        logger.info(f"resp of {url=} {job_id=} is {resp.json()}")
        resp = resp.json()["data"]
        intents = resp["intents"]
        new_content = resp["resp"].strip()
        status = resp["status"]
        # if status != "PENDING":
        if not first_token_cost and new_content:
            first_token_cost = time.time() - start
        content += new_content
        total_cost = time.time() - start
        if total_cost >= timeout:
            break
        if status in ("FINISHED", "FAILED"):
            break
        time.sleep(interval)

    detail = dict(session_id=job_id.split("-")[0], first_token_cost=first_token_cost,
                  content=content, intents=intents, total_cost=total_cost, total_words=total_words)
    return detail


def request_chatbot(data, url, version, sync):
    start = time.time()
    url = url.replace("/chat", "/v2/chat") if version == "v2" else url
    # logger.info(f"response from {url=}")
    try:
        if sync:
            resp = requests.post(url=url, json=data)
            resp = resp.json()

            logger.info(f"response from {url=}:\n{jdumps(resp)}")
            content = resp["data"]["resp"]
            intents = resp["data"].get("intents", [])
            resp = dict(content=content, intents=intents)

        else:
            create_url = url+"/create"
            logger.info(f"request to {create_url=} with data:\n{jdumps(data)}")
            resp = requests.post(url=create_url, json=data)
            resp.raise_for_status()

            logger.info(f"response from {create_url=}:\n{jdumps(resp.json())}")
            job_id = resp.json()["data"]["job_id"]
            resp = gen_with_job_id(
                job_id=job_id, url=url, start=start, detail=True, interval=0.)
    except Exception as e:
        logger.exception(e)
        # logger.info(e)
        return dict()
    return resp


# url = "http://10.50.244.118:5001/v2/chat"


def pef_test(item, url):
    prompt = item["query"]
    session_id = str(time.time()) + "perf"
    data = {
        "prompt": prompt,
        "session_id": session_id,
        "context": {"lon": 121.65187, "lat": 31.25092},
        "character": "车载助手",
    }
    logger.info(f"trace {data}")
    resp_item = request_chatbot(
        data=data, url=url, version="v2", sync=False
    )
    resp_item.update(session_id=session_id, data=data,
                     tgt_domain=item["domain"])
    return resp_item


def get_micro_avg(set_eval_list):
    tp = sum(e['tp'] for e in set_eval_list)
    fp = sum(e['fp'] for e in set_eval_list)
    fn = sum(e['fn'] for e in set_eval_list)
    rs_dict = dict(tp=tp, fp=fp, fn=fn)
    pr_dict = get_pr(tp, fp, fn)
    rs_dict.update(**pr_dict)
    rs_dict.update(f1=get_f1(rs_dict['precision'], rs_dict['recall']))
    return rs_dict


def get_macro_avg(set_eval_list):
    precision_list = [e['precision']
                      for e in set_eval_list if e['tp'] + e['fp'] > 0]
    recall_list = [e['recall'] for e in set_eval_list if e['tp'] + e['fn'] > 0]
    precision = sum(precision_list) / \
        len(precision_list) if precision_list else 0.
    recall = sum(recall_list) / len(recall_list) if recall_list else 0.
    f1 = get_f1(precision, recall)
    rs_dict = dict(precision=precision, recall=recall, f1=f1)
    return rs_dict


def statistic(items):

    true_sets = [(idx, e['tgt_domain'])
                 for idx, e in enumerate(items) if e['tgt_domain']]
    pred_sets = [(idx, e['intents'][0]["domain"])
                 for idx, e in enumerate(items) if e['tgt_domain']]

    true_label_dict = groupby(true_sets, key=lambda x: x[1])
    pred_label_dict = groupby(pred_sets, key=lambda x: x[1])

    target_type_set = true_label_dict.keys() | pred_label_dict.keys()
    detail_dict = dict()
    for target_type in target_type_set:
        true_list = true_label_dict.get(target_type, [])
        true_set = set(true_list)
        pred_list = pred_label_dict.get(target_type, [])
        pred_set = set(pred_list)
        eval_rs = eval_sets(true_set, pred_set)
        detail_dict[target_type] = eval_rs
    detail_dict = dict(
        sorted(detail_dict.items(), key=lambda x: x[1]["f1"], reverse=True))
    set_eval_list = detail_dict.values()
    micro_eval_rs = get_micro_avg(set_eval_list)
    macro_eval_rs = get_macro_avg(set_eval_list)
    rs_dict = dict(detail=detail_dict, micro=micro_eval_rs,
                   macro=macro_eval_rs)
    avg_latency = sum(e["total_cost"] for e in items) / len(items)
    avg_first_token_latency = sum(e["first_token_cost"]
                                  for e in items) / len(items)

    rs_dict.update(avg_first_token_latency=avg_first_token_latency,
                   avg_latency=avg_latency)
    return rs_dict


@click.command()
@click.option("--input_path", default="data/test.jsonl")
@click.option("--work_num", default=1)
@click.option("--url", default="https://langchain.bigmodel.cn/im_chat/chat")
def main(input_path="data/test.jsonl", work_num=1, url="https://langchain.bigmodel.cn/im_chat/chat"):
    output_path = input_path.replace(
        ".jsonl", f"{time.time()}.pef{work_num}.jsonl")
    output_path = output_path.replace("data", "output")

    querys = jload_lines("data/test.jsonl")
    st = time.time()
    querys = querys[:]

    func = batch_process(work_num=work_num, return_list=True)(pef_test)
    rs = func(data=querys, url=url)
    # logger.info(rs)
    cost = time.time() - st
    stat = statistic(rs)

    stat.update(test_cost=cost, test_num=len(querys), qps=len(querys)/cost)
    rs.append(stat)

    logger.info(f"dump to {output_path}")
    jdump(rs, output_path)
    logger.info(f"done")


if __name__ == "__main__":
    main()
