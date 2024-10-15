#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/8/2
# @Author  : yanxiaodong
# @File    : model_metadata_update.py
"""
import os
from typing import Dict, List
from collections import defaultdict
import yaml

import bcelogger
from pygraphv1.client.graph_api_graph import GraphContent
from windmillmodelv1.client.model_api_model import Category, Label


def update_metadata(graph: GraphContent, model_metadata: Dict, input_uri: str = "/home/windmill/tmp/model"):
    """
    Update the model metadata.
    """
    # 1. 获取后处理节点
    model_name = None
    category = None
    for node in graph.nodes:
        for property_ in node.properties:
            if property_.name == "localName":
                model_name = property_.value
            if property_.name == "category" and property_.value == Category.CategoryImagePostprocess.value:
                category = property_.value
        if model_name is not None and category is not None:
            break
    assert category is not None, "No postprocess model found"
    bcelogger.info(f"Postprocess model name: {model_name}, category: {category}")

    # 2. 解析后处理节点
    labels = []
    label_dict = defaultdict(set)
    filepath = os.path.join(input_uri, model_name, "parse.yaml")
    data = yaml.load(open(filepath, "r"), Loader=yaml.FullLoader)
    assert len(data["outputs"]) > 0, f"No output found in {data}"
    assert "fields_map" in data["outputs"][0], f'Field fields_map not in {data["outputs"][0]}'

    for item in data["outputs"][0]["fields_map"]:
        if len(item["categories"]) == 0:
            continue
        elif isinstance(item["categories"][0], list):
            for sub_item in item["categories"]:
                parse_labels(sub_item, label_dict, item["model_name"], labels)
        elif isinstance(item["categories"][0], dict):
            parse_labels(item["categories"], label_dict, item["model_name"], labels)
        else:
            bcelogger.error(f'Model name {item["model_name"]} labels {item["categories"]} is invalid')

    model_metadata["labels"] = labels
    model_metadata["graphContent"] = graph.dict(by_alias=True, exclude_none=True)


def parse_labels(model_labels: List[Dict], label_dict: Dict, model_name: str, labels: List[Dict]):
    """
    Parse the labels.
    """
    label_name2id = {}
    start_idx = 0
    new_model_labels = []
    for label in model_labels:
        bcelogger.info(f'Model {model_name} label: {label}')

        if "display_name" in label:
            label["id"] = int(label["id"])
        elif "display_name" not in label and "super_category" not in label:
            label["display_name"] = label["name"]
            label["name"] = label["id"]
            label["id"] = len(label_dict) + start_idx
            start_idx += 1
        else:
            label["display_name"] = label["name"]
            label["name"] = label["id"]
            label["id"] = start_idx
            start_idx += 1
        new_model_labels.append(label)

        if "super_category" in label:
            if label["super_category"] not in label_name2id:
                label_name2id[label["super_category"]] = len(label_dict)
                new_model_labels.append({"id": len(label_dict),
                                         "name": label["super_category"],
                                         "display_name": label["super_category"]})

    for label in new_model_labels:
        if "super_category" not in label and label["name"] in label_dict and label["name"] not in label_dict:
            continue
        if "super_category" in label and label["name"] in label_dict.get(label["super_category"], set()):
            continue

        if "super_category" in label:
            label_dict[label["super_category"]].add(label["name"])
        else:
            label_dict[label["name"]] = label_dict.get(label["name"], set())

        if "super_category" in label:
            labels.append(Label(id=label["id"],
                                name=label["name"],
                                displayName=label["display_name"],
                                parentID=label_name2id[label["super_category"]]).dict(by_alias=True, exclude_none=True))
        else:
            labels.append(Label(id=label["id"],
                                name=label["name"],
                                displayName=label["display_name"]).dict(by_alias=True, exclude_none=True))
