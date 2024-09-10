/*
 * Tencent is pleased to support the open source community by making
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) available.
 *
 * Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
 *
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) is licensed under the MIT License.
 *
 * License for 蓝鲸智云PaaS平台 (BlueKing PaaS):
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
import { ref, Ref } from 'vue';

import { debounce } from 'lodash';
import tippy from 'tippy.js';

export default class PopInstanceUtil {
  private tippyInstance;
  private refContent: Ref<{ $el?: HTMLElement }> = ref(null);
  private onShowFn;
  private onHiddenFn;
  private arrow = true;
  private newInstance = true;
  private tippyOptions = {};

  private delayShowInstance;

  constructor({ refContent, onShowFn, onHiddenFn, arrow = true, newInstance = true, tippyOptions = {} }) {
    this.tippyInstance = null;
    this.refContent = refContent;
    this.onShowFn = onShowFn;
    this.onHiddenFn = onHiddenFn;
    this.arrow = arrow;
    this.newInstance = newInstance;
    this.tippyOptions = tippyOptions;

    /**
     * 处理多次点击触发多次请求的事件
     */
    this.delayShowInstance = debounce(target => {
      this.initInistance(target);
      this.getTippyInstance()?.show();
    });
  }

  getTippyInstance() {
    return this.tippyInstance;
  }

  uninstallInstance = () => {
    if (this.tippyInstance) {
      this.tippyInstance.hide();
      this.tippyInstance.unmount();
      this.tippyInstance.destroy();
      this.tippyInstance = null;
    }
  };

  initInistance(target) {
    if (this.newInstance) {
      this.uninstallInstance();
    }

    if (this.tippyInstance === null && this.refContent.value) {
      this.tippyInstance = tippy(target, {
        arrow: this.arrow,
        content: (this.refContent.value?.$el ?? this.refContent.value) as HTMLElement,
        trigger: 'manual',
        theme: 'log-light',
        placement: 'bottom-start',
        interactive: true,
        maxWidth: 800,
        zIndex: (window as any).__bk_zIndex_manager.nextZIndex(),
        onShow: () => {
          this.onShowFn?.(this.tippyInstance);
        },
        onHidden: () => {
          this.onHiddenFn?.();
        },
        ...(this.tippyOptions ?? {}),
      });
    }
  }

  show(target) {
    this.delayShowInstance(target);
  }

  repositionTippyInstance() {
    if (!this.newInstance && this.getTippyInstance()?.state.isShown) {
      this.getTippyInstance()?.popperInstance?.update();
    }
  }

  hide() {
    this.getTippyInstance()?.hide();
  }
}
