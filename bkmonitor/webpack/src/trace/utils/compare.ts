/* eslint-disable no-case-declarations */
/*
 * Tencent is pleased to support the open source community by making
 * 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
 *
 * Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
 *
 * 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) is licensed under the MIT License.
 *
 * License for 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition):
 *
 * ---------------------------------------------------
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of
 * the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
 * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

import { IDiffInfo } from '../typings';

export const COMPARE_DIFF_COLOR_LIST = [
  {
    value: -100,
    color: '#30B897'
  },
  {
    value: -80,
    color: '#55C2A9'
  },
  {
    value: -60,
    color: '#7BCCBB'
  },
  {
    value: -40,
    color: '#9FD7CC'
  },
  {
    value: -20,
    color: '#C5E1DE'
  },
  {
    value: 0,
    color: '#DDDFE3'
  },
  {
    value: 20,
    color: '#E9D3D7'
  },
  {
    value: 40,
    color: '#E8BBBE'
  },
  {
    value: 60,
    color: '#E8A4A6'
  },
  {
    value: 80,
    color: '#E88C8D'
  },
  {
    value: 100,
    color: '#E77474'
  }
];
export const COMPARE_ADDED_COLOR = '#46A28C';
export const COMPARE_REMOVED_COLOR = '#D74747';

/**
 * @desc 对比 diff rate 计算
 * @param { Record<string, IDiffInfo> } diffInfo
 * @returns { string }
 */
export const getDiffPercentColor = (diffInfo: Record<string, IDiffInfo>) => {
  const diffInfoList = Object.keys(diffInfo);

  if (['added', 'removed'].includes(diffInfo[diffInfoList[0]].mark)) {
    return diffInfo[diffInfoList[0]].mark === 'added' ? COMPARE_ADDED_COLOR : COMPARE_REMOVED_COLOR;
  }

  if (diffInfo[diffInfoList[0]].mark === 'unchanged') {
    return COMPARE_DIFF_COLOR_LIST[5].color;
  }

  const percentList = diffInfoList.map(info => {
    const { comparison, baseline } = diffInfo[info];
    return ((baseline - comparison) / comparison) * 100;
  });
  const averagePercent = percentList.reduce((acc, val) => acc + val, 0) / percentList.length;
  const colorIndex = COMPARE_DIFF_COLOR_LIST.findIndex(val => val.value > averagePercent);
  if (colorIndex === -1) return COMPARE_DIFF_COLOR_LIST[10].color;
  if (averagePercent > 0) return COMPARE_DIFF_COLOR_LIST[colorIndex].color;
  return COMPARE_DIFF_COLOR_LIST[colorIndex - 1].color;
};

/**
 * @desc 对比 diff rate 计算
 * @param { string } mark
 * @param { number } current
 * @param { number } baseline
 * @returns { string }
 */
export const getSingleDiffColor = ({ mark, comparison, baseline }: IDiffInfo) => {
  switch (mark) {
    case 'added':
      return COMPARE_ADDED_COLOR;
    case 'removed':
      return COMPARE_REMOVED_COLOR;
    case 'unchanged':
      return COMPARE_DIFF_COLOR_LIST[5].color;
    default:
      const percent = ((baseline - comparison) / comparison) * 100;
      const colorIndex = COMPARE_DIFF_COLOR_LIST.findIndex(val => val.value > percent);

      if (colorIndex === -1) return COMPARE_DIFF_COLOR_LIST[10].color;
      if (percent > 0) return COMPARE_DIFF_COLOR_LIST[colorIndex].color;
      return COMPARE_DIFF_COLOR_LIST[colorIndex - 1].color;
  }
};

/** 更新 localStorage 临时对比列表 */
export const updateTemporaryCompareTrace = (traceID: string) => {
  const localList: string[] = [traceID];
  const oldList = JSON.parse(localStorage.getItem('trace_temporary_compare_ids')) || [];
  localList.push(...oldList.slice(0, 5).filter((val: string) => val !== traceID));
  localStorage.setItem('trace_temporary_compare_ids', JSON.stringify(localList.slice(0, 5)));
};
