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
import { Component, Inject, Ref } from 'vue-property-decorator';
import { Component as tsc } from 'vue-tsx-support';
import { Button, Exception, Form, FormItem, Input, Option, Select, Spin, Tag } from 'bk-magic-vue';

import { applicationList, CMDBInfoList, logList, serviceInfo } from '../../../../monitor-api/modules/apm_base_info';
import {
  logServiceRelationBkLogIndexSet,
  serviceConfig,
  serviceUrlList,
  uriregularVerify
} from '../../../../monitor-api/modules/apm_service';
import ChangeRcord from '../../../../monitor-pc/components/change-record/change-record';
import PanelItem from '../../../components/panel-item/panel-item';
import {
  IAppInfoItem,
  IBaseParams,
  ICmdbInfoItem,
  ICmdbRelation,
  IIndexSetItem,
  ILocationRelation,
  ILogInfoItem,
  IServiceInfo
} from '../../../typings';
import * as authorityMap from '../../home/authority-map';

import DebuggerDialog from './debugger-dialog';

import './basic-info.scss';

@Component
export default class BasicInfo extends tsc<{}> {
  @Ref() logForm: any;
  @Ref() appForm: any;
  @Ref() apdexForm: any;

  @Inject('authority') authority;
  @Inject('handleShowAuthorityDetail') handleShowAuthorityDetail;

  isLoading = false;
  isSubmitLoading = false;
  showDebuggerDialog = false;
  urlListLoading = false;
  isDebugging = false;
  debugged = false;
  /** 编辑态 */
  isEditing = false;
  /** 操作记录弹窗配置 */
  record: {
    data: Record<string, string>;
    show: boolean;
  } = {
    show: false,
    data: {}
  };
  params: IBaseParams = {
    // 全局参数
    app_name: '',
    service_name: '',
    bk_biz_id: -1
  };
  serviceInfo: IServiceInfo = {
    topo_key: '',
    instance_count: 0,
    extra_data: {
      category_name: '',
      category_icon: '',
      predicate_value: '',
      predicate_value_icon: '',
      service_language: ''
    },
    relation: {}
  };
  /** cmdb列表 */
  cmdbInfoList: ICmdbInfoItem[] = [];
  /** 日志列表 */
  logsInfoList: ILogInfoItem[] = [];
  /** 应用列表 */
  appList: IAppInfoItem[] = [];
  localRelationInfo: ILocationRelation = {
    cmdb: '',
    logType: '',
    logValue: '',
    relatedBizId: 0,
    bizId: '',
    appId: '',
    apdex: 0
  };
  localCmdbRelationTag: ICmdbRelation = {
    id: -1,
    template_id: -1,
    template_name: '',
    first_category: {
      name: '',
      icon: ''
    },
    second_category: {
      name: '',
      icon: ''
    }
  };
  /** 索引集列表 */
  indexSetList: IIndexSetItem[] = [];
  uriList: string[] = [];
  /** uri源数据 */
  urlResource = '';
  /** 调试结果列表 */
  debuggerResult: string[] | null = null;
  /** 拖拽数据 */
  dragData: { from: number; to: number } = {
    from: null,
    to: null
  };
  drag = {
    active: -1
  };
  rules = {
    logValue: [
      {
        validator: val => !(this.localRelationInfo.logType && val.trim?.() === ''),
        message:
          this.localRelationInfo.logType === 'bk_log' ? window.i18n.t('输入关联日志') : window.i18n.t('选择索引集'),
        trigger: 'blur'
      }
    ],
    relatedBizId: [
      {
        validator: val => !(this.localRelationInfo.logType && val.trim?.() === ''),
        message: window.i18n.t('选择业务'),
        trigger: 'blur'
      }
    ],
    appId: [
      {
        validator: val => !(this.localRelationInfo.bizId && !val),
        message: window.i18n.t('选择应用'),
        trigger: 'blur'
      }
    ],
    apdex: [
      {
        required: true,
        message: window.i18n.tc('必填项'),
        trigger: 'blur'
      },
      {
        validator: val => /^[0-9]*$/.test(val),
        message: window.i18n.t('仅支持数字'),
        trigger: 'blur'
      }
    ]
  };

  get bizSelectList() {
    return this.$store.getters.bizList.map(el => ({
      id: el.id,
      name: el.text
    }));
  }

  created() {
    const { query } = this.$route;
    this.params = {
      app_name: query.app_name as string,
      service_name: query.service_name as string,
      bk_biz_id: this.$store.getters.bizId
    };
    this.getCMDBSelectList();
    this.getLogSelectList();
    this.getServiceInfo();
    this.getUriSourceData();
  }

  /**
   * @desc 获取uri源数据
   */
  async getUriSourceData() {
    this.urlListLoading = true;
    const data = await serviceUrlList({
      app_name: this.params.app_name,
      service_name: this.params.service_name
    }).catch(() => []);
    this.urlResource = data.join('\n');
    this.urlListLoading = false;
  }
  /**
   * @desc: 获取CMDB分类下拉列表
   */
  async getCMDBSelectList() {
    const data = await CMDBInfoList(this.params).catch(() => []);
    this.cmdbInfoList = data;
  }
  /**
   * @desc: 获取日志列表
   */
  async getLogSelectList() {
    const data = await logList(this.params).catch(() => []);
    this.logsInfoList = data;
  }
  /**
   * @desc: 切换关联日志
   */
  handleRelationLogChange() {
    this.localRelationInfo.logValue = '';
    this.logForm.clearError();
  }
  /**
   * @desc: 切换关联业务
   */
  async handleBizChange(v) {
    this.localRelationInfo.appId = '';
    this.appForm?.clearError();
    if (v) {
      const data = await applicationList({ bk_biz_id: this.localRelationInfo.bizId }).catch(() => []);
      this.appList = data;
    }
  }
  /**
   * @desc: 获取服务基础信息
   */
  async getServiceInfo() {
    this.isLoading = true;
    const data = await serviceInfo(this.params).catch(() => {});
    const {
      topo_key: topoKey,
      extra_data: extraData,
      relation,
      created_by: createUser,
      created_at: createTime,
      updated_by: updateUser,
      updated_at: updateTime
    } = data;
    this.record.data = { createUser, createTime, updateTime, updateUser };
    this.uriList = (relation.uri_relation || []).map(item => item.uri);
    Object.assign(this.serviceInfo, {
      topo_key: topoKey,
      extra_data: extraData || {},
      relation
    });
    this.setRelationInfo();
    this.isLoading = false;
  }
  /**
   * @desc: 设置编辑时关联信息表单
   */
  async setRelationInfo() {
    const {
      cmdb_relation: cmdbRelation,
      log_relation: logRelation,
      app_relation: appRelation,
      apdex_relation: apdexRelation
    } = this.serviceInfo.relation;

    if (cmdbRelation.template_id) {
      // CMDB关联
      this.localRelationInfo.cmdb = cmdbRelation.template_id;
      this.handleCmdbChange(this.localRelationInfo.cmdb);
    }
    if (logRelation.log_type) {
      // 关联日志
      this.localRelationInfo.logType = logRelation.log_type;
      this.localRelationInfo.logValue = logRelation.value;
      if (logRelation.log_type === 'bk_log') {
        this.localRelationInfo.relatedBizId = logRelation.related_bk_biz_id;
        await this.handleLogBizChange(logRelation.related_bk_biz_id);
        this.localRelationInfo.logValue = logRelation.value;
      }
    }
    if (appRelation.relate_bk_biz_id) {
      // 关联应用
      this.localRelationInfo.bizId = appRelation.relate_bk_biz_id;
      await this.handleBizChange(this.localRelationInfo.bizId);
      this.localRelationInfo.appId = appRelation.application_id;
    }
    // Apdex
    this.localRelationInfo.apdex = apdexRelation?.apdex_value;
  }
  /**
   * @desc: CMDB关联变更
   */
  handleCmdbChange(v) {
    if (v) {
      const curRelation = this.cmdbInfoList.find(item => item.id === v);
      if (curRelation) {
        this.localCmdbRelationTag = {
          ...curRelation,
          template_name: curRelation.name
        };
      }
    } else {
      this.localCmdbRelationTag = {
        id: -1,
        template_id: -1,
        template_name: '',
        first_category: {
          name: '',
          icon: ''
        },
        second_category: {
          name: '',
          icon: ''
        }
      };
    }
  }
  async handleEditClick(show: boolean) {
    this.isEditing = show;
    if (show) {
      // 如果URI为空 则编辑时添加一项空 可输入
      if (!this.uriList.length) {
        this.uriList.push('');
      }
    } else {
      // 如果URI为空 则删除该列展示
      this.uriList = this.uriList.filter(val => val.trim?.().length);
    }
  }
  /**
   * @desc 切换关联日志应用
   * @param { number } v
   */
  async handleLogBizChange(v) {
    this.localRelationInfo.logValue = '';
    this.logForm?.clearError();
    const data = await logServiceRelationBkLogIndexSet({
      bk_biz_id: v
    }).catch(() => []);
    this.indexSetList = data;
  }
  /** 增/删URI */
  handleChangeUri(handle: string, index: number) {
    if (handle === 'add') {
      this.uriList.splice(index + 1, 0, '');
      return;
    }

    if (this.uriList.length === 1) {
      return;
    }

    this.uriList.splice(index, 1);
  }
  /** 输入uri */
  handleUriInput(val: string, index: number) {
    this.uriList[index] = val;
  }
  /**
   * @desc uri调试
   */
  async handlDebugger() {
    const uris = this.uriList.filter(item => item.trim?.());
    const urlSourceList = this.urlResource.split(/[(\r\n)\r\n]+/).filter(val => val) || [];
    const params = {
      ...this.params,
      uris,
      uris_source: urlSourceList
    };
    this.isDebugging = true;
    this.debugged = true;
    await uriregularVerify(params)
      .then(data => {
        this.debuggerResult = data || [];
      })
      .catch(() => {
        this.debuggerResult = null;
      })
      .finally(() => {
        this.isDebugging = false;
      });
  }
  /**
   * @description: 拖拽开始
   * @param {DragEvent} evt
   * @param {number} index
   */
  handleDragStart(evt: DragEvent, index: number) {
    this.dragData.from = index;
    // eslint-disable-next-line no-param-reassign
    evt.dataTransfer.effectAllowed = 'move';
  }

  /**
   * @description: 拖拽结束
   */
  handleDragend() {
    // 动画结束后关闭拖拽动画效果
    setTimeout(() => {
      this.dragData.from = null;
      this.dragData.to = null;
    }, 500);
    this.drag.active = -1;
  }
  /**
   * @description: 拖拽放入
   */
  handleDrop() {
    const { from, to } = this.dragData;
    if (from === to || [from, to].includes(null)) return;
    const temp = this.uriList[from];
    this.uriList.splice(from, 1);
    this.uriList.splice(to, 0, temp);
    this.drag.active = -1;
  }
  /**
   * @description: 拖拽进入
   * @param {number} index
   */
  handleDragEnter(index: number) {
    this.dragData.to = index;
  }
  /**
   * @description: 拖拽经过
   * @param {DragEvent} evt
   */
  handleDragOver(evt: DragEvent, index: number) {
    evt.preventDefault();
    this.drag.active = index;
  }
  /**
   * @description: 拖拽离开
   */
  handleDragLeave() {
    this.drag.active = -1;
  }
  /** 获取提交参数 */
  getParams() {
    const params: any = {
      ...this.params,
      uri_relation: [],
      apdex_relation: {
        apdex_value: Number(this.localRelationInfo.apdex)
      }
    };
    // 关联CMDB
    if (this.localRelationInfo.cmdb) {
      params.cmdb_relation = {
        template_id: this.localRelationInfo.cmdb
      };
    }
    // 关联日志
    if (this.localRelationInfo.logType) {
      const { logType, logValue, relatedBizId } = this.localRelationInfo;
      params.log_relation = {
        log_type: logType,
        value: logValue,
        related_bk_biz_id: relatedBizId
      };
      if (logType !== 'bk_log') delete params.related_bk_biz_id;
    }
    // 关联应用
    if (this.localRelationInfo.bizId) {
      const { bizId, appId } = this.localRelationInfo;
      params.app_relation = {
        relate_bk_biz_id: bizId,
        relate_app_name: appId
      };
    }
    // uri 信息
    if (this.uriList.length) {
      params.uri_relation = this.uriList.filter(val => val?.trim() !== '');
    }

    return params;
  }
  /** 提交保存 */
  async handleSubmit() {
    const promiseList = ['logForm', 'appForm', 'apdexForm'].map(item => this[item]?.validate());
    await Promise.all(promiseList)
      .then(async () => {
        const params = this.getParams();
        this.isSubmitLoading = true;
        await serviceConfig(params)
          .then(() => {
            this.$bkMessage({
              message: this.$t('保存成功'),
              theme: 'success'
            });
            this.handleEditClick(false);
            this.getServiceInfo();
          })
          .finally(() => {
            this.isSubmitLoading = false;
          });
      })
      .catch(err => {
        console.warn(err);
      });
  }

  render() {
    const {
      cmdb_relation: cmdbRelation,
      log_relation: logRelation,
      app_relation: appRelation
    } = this.serviceInfo.relation;
    const curCmdbRelationTagList = this.isEditing ? this.localCmdbRelationTag : cmdbRelation;
    const getResultContent = () => {
      if (!this.debugged || !this.debuggerResult) return '';

      if (this.debuggerResult?.length)
        return this.debuggerResult.map(item => (
          <span>
            {item}
            <br />
          </span>
        ));

      return (
        <Exception
          class='empty-result'
          type='empty'
          scene='part'
        >
          <span>{this.$t('暂无匹配')}</span>
        </Exception>
      );
    };

    return (
      <div
        class={['conf-content base-info-wrap']}
        v-bkloading={{ isLoading: this.isLoading }}
      >
        <PanelItem title={this.$t('基础信息')}>
          <div class='form-content'>
            <div class='info-wrap'>
              <div class='config-form-item'>
                <label class='label'>{this.$t('服务名称')}</label>
                <div class='content'>{this.serviceInfo.topo_key || '--'}</div>
              </div>
              <div class='config-form-item'>
                <label class='label'>{this.$t('一级分类')}</label>
                <div class='content'>
                  <img
                    class='category-icon'
                    src={this.serviceInfo.extra_data?.category_icon}
                  />
                  <span class='category-name'>{this.serviceInfo.extra_data?.category_name}</span>
                </div>
              </div>
              <div class='config-form-item'>
                <label class='label'>{this.$t('二级分类')}</label>
                <div class='content'>{this.serviceInfo.extra_data?.predicate_value || '--'}</div>
              </div>
              <div class='config-form-item'>
                <label class='label'>{this.$t('语言')}</label>
                <div class='content'>
                  <div class='content'>{this.serviceInfo.extra_data?.service_language || '--'}</div>
                </div>
              </div>
              <div class='config-form-item'>
                <label class='label'>{this.$t('实例数')}</label>
                <div class='content'>{this.serviceInfo.instance_count || 0}</div>
              </div>
            </div>
          </div>
        </PanelItem>
        <PanelItem title={this.$t('关联设置')}>
          <div class={['form-content relation-info', { 'is-editing': this.isEditing }]}>
            <div class='config-form-item'>
              <label class='label'>{this.$t('关联服务类型')}</label>
              <div class='content'>
                {this.isEditing && (
                  <div class='edit-form-item'>
                    <Select
                      vModel={this.localRelationInfo.cmdb}
                      searchable
                      onChange={v => this.handleCmdbChange(v)}
                    >
                      {this.cmdbInfoList.map(option => (
                        <Option
                          key={option.id}
                          id={option.id}
                          name={option.name}
                        ></Option>
                      ))}
                    </Select>
                  </div>
                )}
                <div class='tag-list'>
                  <Tag class='relation-info-tag'>
                    <span class='tag-label'>{this.$t('服务名称 :')}</span>
                    <span>{curCmdbRelationTagList?.template_name || '--'}</span>
                  </Tag>
                  <Tag class='relation-info-tag'>
                    <div class='category-tag'>
                      <span class='tag-label'>{this.$t('一级分类 :')}</span>
                      {curCmdbRelationTagList?.first_category?.icon && (
                        <img
                          class='icon'
                          src={curCmdbRelationTagList?.first_category?.icon}
                        />
                      )}
                      <span>{curCmdbRelationTagList?.first_category?.name || '--'}</span>
                    </div>
                  </Tag>
                  <Tag class='relation-info-tag'>
                    <div class='category-tag'>
                      <span class='tag-label'>{this.$t('二级分类 :')}</span>
                      {curCmdbRelationTagList?.second_category?.icon && (
                        <img
                          class='icon'
                          src={curCmdbRelationTagList?.second_category?.icon}
                        />
                      )}
                      <span>{curCmdbRelationTagList?.second_category?.name || '--'}</span>
                    </div>
                  </Tag>
                </div>
              </div>
            </div>
            {this.isEditing && (
              <p class='form-item-tips'>
                {this.$t(
                  '默认会进行自动识别，如果识别错误或者未识别到可以手动进行关联，关联后可以查看对应的主机和进程信息。'
                )}
              </p>
            )}
            <div class='config-form-item'>
              <label class='label'>{this.$t('关联日志')}</label>
              <div class='content'>
                {this.isEditing ? (
                  <div class='edit-form-item'>
                    <Select
                      vModel={this.localRelationInfo.logType}
                      searchable
                      onChange={() => this.handleRelationLogChange()}
                    >
                      {this.logsInfoList.map(option => (
                        <Option
                          key={option.id}
                          id={option.id}
                          name={option.name}
                        ></Option>
                      ))}
                    </Select>
                    <Form
                      ref='logForm'
                      {...{
                        props: {
                          model: this.localRelationInfo,
                          rules: this.rules
                        }
                      }}
                    >
                      {this.localRelationInfo.logType === 'bk_log' ? (
                        <div class='relation-log-select relation-log-form-item'>
                          <FormItem property='relatedBizId'>
                            <Select
                              vModel={this.localRelationInfo.relatedBizId}
                              searchable
                              onChange={v => this.handleLogBizChange(v)}
                            >
                              {this.bizSelectList.map(option => (
                                <Option
                                  key={option.id}
                                  id={option.id}
                                  name={option.name}
                                ></Option>
                              ))}
                            </Select>
                          </FormItem>
                          <FormItem property='logValue'>
                            <Select
                              vModel={this.localRelationInfo.logValue}
                              searchable
                            >
                              {this.indexSetList.map(option => (
                                <Option
                                  key={option.id}
                                  id={option.id}
                                  name={option.name}
                                ></Option>
                              ))}
                            </Select>
                          </FormItem>
                        </div>
                      ) : (
                        <FormItem property='logValue'>
                          <Input
                            class='input'
                            vModel={this.localRelationInfo.logValue}
                          />
                        </FormItem>
                      )}
                    </Form>
                  </div>
                ) : (
                  <section>
                    {logRelation?.value ? (
                      <section>
                        {logRelation?.log_type === 'bk_log' ? (
                          <section>
                            <Tag class='relation-info-tag'>
                              <span>{`${logRelation.log_type_alias} : ${logRelation.related_bk_biz_name}`}</span>
                            </Tag>
                            <Tag class='relation-info-tag'>
                              <span>{`${this.$t('索引集 : ')}${logRelation.value_alias}`}</span>
                            </Tag>
                          </section>
                        ) : (
                          <Tag class='relation-info-tag'>
                            <span>{`${logRelation.log_type_alias} : ${logRelation.value}`}</span>
                          </Tag>
                        )}
                      </section>
                    ) : (
                      '--'
                    )}
                  </section>
                )}
              </div>
            </div>
            {this.isEditing && <p class='form-item-tips'>{this.$t('日志关联后在服务的tab页可以直接查看和使用。')}</p>}
            <div class='config-form-item'>
              <label class='label'>{this.$t('关联应用')}</label>
              <div class='content'>
                {this.isEditing ? (
                  <div class='edit-form-item app-form-item'>
                    <Select
                      vModel={this.localRelationInfo.bizId}
                      searchable
                      onChange={v => this.handleBizChange(v)}
                    >
                      {this.bizSelectList.map(option => (
                        <Option
                          key={option.id}
                          id={option.id}
                          name={option.name}
                        ></Option>
                      ))}
                    </Select>
                    <Form
                      ref='appForm'
                      {...{
                        props: {
                          model: this.localRelationInfo,
                          rules: this.rules
                        }
                      }}
                    >
                      <FormItem property='appId'>
                        <Select
                          style='width:290px'
                          vModel={this.localRelationInfo.appId}
                          searchable
                        >
                          {this.appList.map(option => (
                            <Option
                              key={option.id}
                              id={option.id}
                              name={option.name}
                            ></Option>
                          ))}
                        </Select>
                      </FormItem>
                    </Form>
                  </div>
                ) : (
                  <section>
                    {appRelation?.relate_bk_biz_name && appRelation?.relate_app_name ? (
                      <section>
                        <Tag class='relation-info-tag'>{`${this.$t('业务名称 : ')}${
                          appRelation.relate_bk_biz_name
                        }`}</Tag>
                        <Tag class='relation-info-tag'>{`${this.$t('应用 : ')}${appRelation.relate_app_name}`}</Tag>
                      </section>
                    ) : (
                      '--'
                    )}
                  </section>
                )}
              </div>
            </div>
            {this.isEditing && (
              <p class='form-item-tips'>
                {this.$t(
                  '当某个服务关联另外一个应用，关联后可以从当前服务跳转到下一个应用，实现在不同的应用拓扑进行问题的定位。'
                )}
              </p>
            )}
          </div>
        </PanelItem>
        <PanelItem
          title={this.$t('Apdex设置')}
          flexDirection='column'
        >
          <div
            class='panel-intro'
            style='position:relative'
          >
            <div>
              {this.$t(
                'Apdex（Application Performance Index）是由 Apdex 联盟开发的用于评估应用性能的工业标准。Apdex 标准从用户的角度出发，将对应用响应时间的表现，转为用户对于应用性能的可量化范围为 0-1 的满意度评价。'
              )}
            </div>
            <div>
              {this.$t(
                'Apdex 定义了应用响应时间的最优门槛为 T（即 Apdex 阈值，T 由性能评估人员根据预期性能要求确定），根据应用响应时间结合 T 定义了三种不同的性能表现：'
              )}
            </div>
            <div class='indentation-text'>{`● Satisfied ${this.$t('（满意）- 应用响应时间低于或等于')} T`}</div>
            <div class='indentation-text'>{`● Tolerating ${this.$t(
              '（可容忍）- 应用响应时间大于 T，但同时小于或等于'
            )} 4T`}</div>
            <div class='indentation-text'>{`● Frustrated ${this.$t('（烦躁期）- 应用响应时间大于')} 4T`}</div>
          </div>
          <div class={['form-content apdex-info', { 'is-editing': this.isEditing }]}>
            <div class='config-form-item'>
              <label class='label'>{this.$t('Apdex阈值T')}</label>
              <div class='content'>
                {this.isEditing ? (
                  <div class='edit-form-item apdex-form-item'>
                    <Form
                      ref='apdexForm'
                      {...{
                        props: {
                          model: this.localRelationInfo,
                          rules: this.rules
                        }
                      }}
                    >
                      <FormItem property='apdex'>
                        <Input
                          vModel={this.localRelationInfo.apdex}
                          type='number'
                          show-controls={false}
                        >
                          <template slot='append'>
                            <div class='right-unit'>ms</div>
                          </template>
                        </Input>
                      </FormItem>
                    </Form>
                  </div>
                ) : (
                  this.serviceInfo.relation?.apdex_relation?.apdex_value || 0
                )}
              </div>
            </div>
            {this.isEditing && (
              <p
                class='form-item-tips'
                style='top:-10px'
              >
                {this.$t('默认继承应用的类型设置')}
              </p>
            )}
          </div>
        </PanelItem>
        <PanelItem
          title={this.$t('URI规则设置')}
          class='uri-panel'
          flexDirection='column'
        >
          <div
            class='panel-intro'
            style='position:relative'
          >
            {this.$t(
              '默认取URL中的URI进行统计，实际生产中有很多将ID应用到URI中，所以需要通过手动设置将同一类URI进行归类统计。 如： /user/{ID}/index.html'
            )}
          </div>
          <div
            class='uri-source-content'
            v-bkloading={{ isLoading: this.urlListLoading }}
          >
            <div class='header-tool'>
              <label>{this.$t('URI源')}</label>
              {/* eslint-disable-next-line @typescript-eslint/no-misused-promises */}
              <span
                class='right-btn-wrap'
                slot='headerTool'
                onClick={() => this.getUriSourceData()}
              >
                <i class='icon-monitor icon-shuaxin'></i>
                {this.$t('button-刷新')}
              </span>
            </div>
            <div class='source-box'>
              <Input
                class='source-input'
                type='textarea'
                placeholder=' '
                disabled={!this.isEditing}
                v-model={this.urlResource}
              />
            </div>
          </div>
          <div class={`uri-info ${!this.uriList.length ? 'is-empty' : ''}`}>
            {this.isEditing && <label class='uri-set-label'>{this.$t('URI配置')}</label>}
            <transition-group
              name={this.dragData.from !== null ? 'flip-list' : 'filp-list-none'}
              tag='ul'
            >
              {this.uriList.map((item, index) => (
                <li
                  class={['config-form-item', { 'is-editing': this.isEditing }]}
                  key={index}
                  draggable={this.isEditing}
                  onDragstart={evt => this.handleDragStart(evt, index)}
                  onDragend={this.handleDragend}
                  onDrop={this.handleDrop}
                  onDragenter={() => this.handleDragEnter(index)}
                  onDragover={evt => this.handleDragOver(evt, index)}
                  onDragleave={this.handleDragLeave}
                >
                  {this.isEditing && <i class='icon-monitor icon-mc-tuozhuai'></i>}
                  <label class='label'>{`URI${index + 1}`}</label>
                  <div class='content'>
                    {this.isEditing ? (
                      <div class='edit-uri-row'>
                        <Input
                          class='uri-input'
                          vModel={item}
                          onChange={v => this.handleUriInput(v, index)}
                        />
                        <i
                          class='icon-monitor icon-mc-plus-fill'
                          onClick={() => this.handleChangeUri('add', index)}
                        />
                        <i
                          class={['icon-monitor icon-mc-minus-plus', { disabled: this.uriList.length === 1 }]}
                          onClick={() => this.handleChangeUri('delete', index)}
                        />
                      </div>
                    ) : (
                      item
                    )}
                  </div>
                </li>
              ))}
            </transition-group>
            {this.isEditing && (
              <div class='debugging-content'>
                <div class='header-tool'>
                  <Button
                    outline
                    theme='primary'
                    size='small'
                    loading={this.isDebugging}
                    onClick={() => this.handlDebugger()}
                  >
                    {this.$t('调试')}
                  </Button>
                  {this.debugged && (
                    <div>
                      {this.isDebugging ? (
                        <span class='status-wrap'>
                          <Spin size='mini' />
                          <span style='margin-left:6px;'>{this.$t('调试中')}</span>
                        </span>
                      ) : (
                        <span class='status-wrap'>
                          <i
                            class={`icon-monitor ${this.debuggerResult ? 'icon-mc-check-fill' : 'icon-mc-close-fill'}`}
                          />
                          <span>{this.debuggerResult ? this.$t('调试成功') : this.$t('调试失败')}</span>
                        </span>
                      )}
                    </div>
                  )}
                </div>
                <div class='result-box'>{getResultContent()}</div>
              </div>
            )}
            {!this.isEditing && !this.uriList.length && (
              <Exception
                class='empty-uri-info'
                type='empty'
                scene='part'
              >
                <span>{this.$t('当前未配置URI信息')}</span>
              </Exception>
            )}
          </div>
        </PanelItem>
        <div class='header-tools'>
          {!this.isEditing && (
            <Button
              class='edit-btn'
              theme='primary'
              size='normal'
              outline
              v-authority={{ active: !this.authority }}
              onClick={() => {
                this.authority ? this.handleEditClick(true) : this.handleShowAuthorityDetail(authorityMap.MANAGE_AUTH);
              }}
            >
              {this.$t('button-编辑')}
            </Button>
          )}
          <div
            class='history-btn'
            v-bk-tooltips={{ content: this.$t('变更记录') }}
            onClick={() => (this.record.show = true)}
          >
            <i class='icon-monitor icon-lishijilu'></i>
          </div>
        </div>
        {this.isEditing ? (
          <div class='submit-handle'>
            <Button
              class='mr10'
              theme='primary'
              loading={this.isSubmitLoading}
              onClick={() => this.handleSubmit()}
            >
              {this.$t('保存')}
            </Button>
            <Button onClick={() => this.handleEditClick(false)}>{this.$t('取消')}</Button>
          </div>
        ) : (
          <div></div>
        )}
        <ChangeRcord
          recordData={this.record.data}
          show={this.record.show}
          onUpdateShow={v => (this.record.show = v)}
        />
        <DebuggerDialog v-model={this.showDebuggerDialog} />
      </div>
    );
  }
}
