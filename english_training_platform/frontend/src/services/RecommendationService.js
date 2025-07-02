import MaterialService from './MaterialService';

/**
 * 推荐服务 - 用于获取和处理学习材料推荐
 */
class RecommendationService {
          constructor() {
                    // MaterialService可能是一个单例实例而不是类
                    this.materialService = MaterialService;
                    // 缓存可用材料列表
                    this.availableMaterials = null;
          }

          /**
           * 获取所有可用的材料ID
           * @returns {Promise<Array>} 可用材料ID列表
           */
          async getAvailableMaterialIds() {
                    if (this.availableMaterials) {
                              return this.availableMaterials;
                    }

                    try {
                              const response = await fetch('/materials/index.json');
                              if (!response.ok) {
                                        throw new Error('无法获取材料索引');
                              }

                              const indexData = await response.json();
                              this.availableMaterials = indexData.available_materials || [];

                              // 如果available_materials不存在或为空，尝试从materials_details提取
                              if (!this.availableMaterials.length && indexData.materials_details) {
                                        this.availableMaterials = indexData.materials_details.map(material => material.id);
                              }

                              // 如果仍然为空，使用latest_materials
                              if (!this.availableMaterials.length && indexData.latest_materials) {
                                        this.availableMaterials = indexData.latest_materials.map(material => material.id);
                              }

                              console.log('可用材料列表:', this.availableMaterials);
                              return this.availableMaterials;
                    } catch (error) {
                              console.error('获取可用材料列表失败:', error);
                              // 返回一个安全的默认列表
                              return ['cet4_001', 'cet6_001', 'ielts_001', 'toefl_001', '2022_06', '2022_09'];
                    }
          }

          /**
           * 获取推荐材料
           * @param {Object} userAnswers 用户答题数据
           * @returns {Promise<Array>} 推荐材料列表
           */
          async getRecommendations(userAnswers) {
                    try {
                              // 获取可用材料列表
                              const availableMaterials = await this.getAvailableMaterialIds();
                              console.log('获取到可用材料列表:', availableMaterials);

                              // 如果有后端API，先尝试从API获取推荐
                              try {
                                        // 向API发送请求时，同时提供可用材料列表
                                        console.log('向API发送推荐请求，包含可用材料列表');
                                        const response = await fetch('http://localhost:5000/api/recommendation/recommend', {
                                                  method: 'POST',
                                                  headers: {
                                                            'Content-Type': 'application/json',
                                                  },
                                                  body: JSON.stringify({
                                                            user_answers: userAnswers,
                                                            availableMaterials: availableMaterials // 提供可用材料列表
                                                  }),
                                                  timeout: 10000
                                        });

                                        if (response.ok) {
                                                  const data = await response.json();
                                                  console.log('API返回的推荐结果:', data);

                                                  // 验证推荐的材料是否都存在
                                                  const validatedRecommendations = await this.validateRecommendations(data.recommendations, availableMaterials);

                                                  if (validatedRecommendations.length > 0) {
                                                            console.log('验证后的有效推荐:', validatedRecommendations);
                                                            return {
                                                                      recommendations: validatedRecommendations,
                                                                      weak_areas: data.weak_areas || [],
                                                                      strong_areas: data.strong_areas || [],
                                                                      performance_score: data.performance_score || 0,
                                                                      improvement_suggestions: data.improvement_suggestions || ''
                                                            };
                                                  } else {
                                                            console.warn('API推荐的材料都不存在，使用本地推荐逻辑');
                                                  }
                                        } else {
                                                  console.warn(`API推荐请求失败，状态码: ${response.status}，使用本地推荐逻辑`);
                                        }
                              } catch (error) {
                                        console.error('获取API推荐时出错:', error);
                                        console.warn('使用本地推荐逻辑');
                              }

                              // 使用本地逻辑生成推荐
                              return await this.generateLocalRecommendations(userAnswers, availableMaterials);
                    } catch (error) {
                              console.error('获取推荐失败:', error);
                              throw error;
                    }
          }

          /**
           * 验证推荐的材料是否存在
           * @param {Array} recommendations 推荐材料列表
           * @param {Array} availableMaterials 可用材料ID列表
           * @returns {Promise<Array>} 有效的推荐材料列表
           */
          async validateRecommendations(recommendations, availableMaterials) {
                    if (!recommendations || !Array.isArray(recommendations)) {
                              console.warn('推荐列表为空或不是数组');
                              return [];
                    }

                    console.log('验证推荐材料:', recommendations);
                    console.log('可用材料列表:', availableMaterials);

                    // 确保我们有可用材料列表
                    if (!availableMaterials || !availableMaterials.length) {
                              availableMaterials = await this.getAvailableMaterialIds();
                    }

                    const validRecommendations = [];

                    for (const recommendation of recommendations) {
                              // 获取材料ID（可能是id或materialId字段）
                              const materialId = recommendation.materialId || recommendation.id;

                              if (!materialId) {
                                        console.warn(`推荐项缺少有效的ID: ${JSON.stringify(recommendation)}`);
                                        continue;
                              }

                              // 检查材料ID是否在可用列表中
                              if (availableMaterials.includes(materialId)) {
                                        // 确保同时有id和materialId字段
                                        const validRecommendation = { ...recommendation };
                                        if (!validRecommendation.id) validRecommendation.id = materialId;
                                        if (!validRecommendation.materialId) validRecommendation.materialId = materialId;

                                        // 确保有有效的match_score值
                                        if (!validRecommendation.match_score || isNaN(validRecommendation.match_score)) {
                                                  console.log(`修复推荐项 ${materialId} 的match_score值`);
                                                  validRecommendation.match_score = 0.7; // 设置默认匹配度
                                        }

                                        validRecommendations.push(validRecommendation);
                                        console.log(`有效推荐材料: ${materialId}, 匹配度: ${validRecommendation.match_score}`);
                              } else {
                                        console.warn(`推荐的材料ID "${materialId}" 不在可用列表中，已从推荐列表中移除`);
                              }
                    }

                    // 如果没有有效推荐，返回默认推荐
                    if (validRecommendations.length === 0) {
                              console.warn('没有有效的推荐，使用默认推荐');
                              return this.getDefaultRecommendations(availableMaterials);
                    }

                    return validRecommendations;
          }

          /**
           * 使用本地逻辑生成推荐
           * @param {Object} userAnswers 用户答题数据
           * @param {Array} availableMaterials 可用材料ID列表
           * @returns {Promise<Array>} 推荐材料列表
           */
          async generateLocalRecommendations(userAnswers, availableMaterials) {
                    try {
                              // 确保我们有可用材料列表
                              if (!availableMaterials || !availableMaterials.length) {
                                        availableMaterials = await this.getAvailableMaterialIds();
                              }

                              // 获取所有可用材料详情
                              const allMaterials = await this.getAllMaterialsDetails();
                              if (!allMaterials || allMaterials.length === 0) {
                                        throw new Error('无法获取材料详情');
                              }

                              // 过滤出可用的材料
                              const availableMaterialDetails = allMaterials.filter(
                                        material => availableMaterials.includes(material.id)
                              );

                              if (availableMaterialDetails.length === 0) {
                                        console.warn('没有可用的材料详情，使用默认推荐');
                                        return this.getDefaultRecommendations(availableMaterials);
                              }

                              // 分析用户答题数据，找出薄弱标签
                              const weakTags = this.analyzeWeakTags(userAnswers);
                              console.log('用户薄弱标签:', weakTags);

                              // 根据薄弱标签推荐材料
                              const recommendations = this.recommendByTags(availableMaterialDetails, weakTags);

                              return recommendations;
                    } catch (error) {
                              console.error('生成本地推荐时出错:', error);
                              // 出错时返回一些默认推荐
                              return this.getDefaultRecommendations(availableMaterials);
                    }
          }

          /**
           * 获取所有材料详情
           * @returns {Promise<Array>} 所有材料详情
           */
          async getAllMaterialsDetails() {
                    try {
                              const response = await fetch('/materials/index.json');
                              if (!response.ok) {
                                        throw new Error('无法获取材料索引');
                              }

                              const indexData = await response.json();
                              return indexData.materials_details || [];
                    } catch (error) {
                              console.error('获取所有材料详情时出错:', error);
                              return [];
                    }
          }

          /**
           * 分析用户答题数据，找出薄弱标签
           * @param {Object} userAnswers 用户答题数据
           * @returns {Array} 薄弱标签列表
           */
          analyzeWeakTags(userAnswers) {
                    if (!userAnswers || !userAnswers.answers) {
                              return ['校园生活', '学术研究', '科技应用']; // 默认标签
                    }

                    // 统计错误答案相关的标签
                    const tagCounts = {};
                    let totalQuestions = 0;
                    let totalIncorrect = 0;

                    // 遍历用户答题数据
                    for (const materialId in userAnswers.answers) {
                              const materialAnswers = userAnswers.answers[materialId];

                              // 获取材料的标签
                              const materialTags = this.getMaterialTagsById(materialId);

                              // 统计错误答案
                              for (const answer of materialAnswers) {
                                        totalQuestions++;
                                        if (!answer.isCorrect) {
                                                  totalIncorrect++;

                                                  // 增加相关标签的计数
                                                  for (const tag of materialTags) {
                                                            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
                                                  }
                                        }
                              }
                    }

                    // 计算错误率
                    const incorrectRate = totalQuestions > 0 ? totalIncorrect / totalQuestions : 0;
                    console.log(`总题数: ${totalQuestions}, 错题数: ${totalIncorrect}, 错误率: ${incorrectRate.toFixed(2)}`);

                    // 按计数排序标签
                    const sortedTags = Object.entries(tagCounts)
                              .sort((a, b) => b[1] - a[1])
                              .map(entry => entry[0]);

                    // 返回前3个薄弱标签，如果不足3个则返回所有
                    return sortedTags.slice(0, 3);
          }

          /**
           * 根据材料ID获取标签
           * @param {string} materialId 材料ID
           * @returns {Array} 标签列表
           */
          getMaterialTagsById(materialId) {
                    // 这里应该从缓存或再次请求获取材料标签
                    // 简化实现，返回一些默认标签
                    const defaultTags = {
                              'cet4_001': ['校园生活', '学生活动', '课程安排', '学习方法', '校园设施'],
                              'cet6_001': ['科技创新', '人工智能', '数字化转型', '技术发展', '科研突破'],
                              'ielts_001': ['环境保护', '可持续发展', '生态系统', '气候变化', '环保政策'],
                              'toefl_001': ['学术讲座', '历史事件', '文化差异', '研究方法', '学术论证'],
                              '2022_06': ['校园生活', '学术研究', '社会现象', '职业发展', '日常对话'],
                              '2022_09': ['科技应用', '环境问题', '社会发展', '创新思维', '公共政策'],
                              '2022_12_1': ['文化传承', '历史事件', '传统习俗', '文化差异', '社会变迁'],
                              '2022_12_02': ['科技发展', '创新应用', '数字化', '未来趋势', '技术突破']
                    };

                    return defaultTags[materialId] || ['校园生活', '学术研究', '科技应用'];
          }

          /**
           * 根据标签推荐材料
           * @param {Array} materials 所有材料
           * @param {Array} tags 标签列表
           * @returns {Array} 推荐材料列表
           */
          recommendByTags(materials, tags) {
                    // 为每个材料计算与标签的匹配度
                    const materialScores = materials.map(material => {
                              let score = 0;

                              // 计算标签匹配分数
                              if (material.tags) {
                                        for (const tag of tags) {
                                                  if (material.tags.includes(tag)) {
                                                            score += 1;
                                                  }
                                        }
                              }

                              return {
                                        materialId: material.id, // 确保使用materialId作为统一属性名
                                        title: material.title,
                                        difficulty: material.difficulty,
                                        score,
                                        match_score: score / Math.max(tags.length, 1), // 添加match_score属性
                                        matchedTags: material.tags ? material.tags.filter(tag => tags.includes(tag)) : []
                              };
                    });

                    // 按匹配度排序
                    const sortedMaterials = materialScores
                              .filter(item => item.score > 0) // 只保留有匹配的材料
                              .sort((a, b) => b.score - a.score);

                    // 返回前5个推荐，如果不足5个则返回所有
                    const recommendations = sortedMaterials.slice(0, 5).map(item => ({
                              materialId: item.materialId, // 使用materialId作为统一属性名
                              id: item.materialId, // 同时提供id属性以兼容
                              title: item.title,
                              difficulty: item.difficulty,
                              match_score: item.match_score, // 添加match_score属性
                              reason: `这个材料包含了您需要加强的主题: ${item.matchedTags.join(', ')}`
                    }));

                    // 如果没有匹配的材料，返回一些默认推荐
                    if (recommendations.length === 0) {
                              return this.getDefaultRecommendations(materials.map(material => material.id));
                    }

                    return recommendations;
          }

          /**
           * 获取默认推荐
           * @param {Array} availableMaterials 可用材料ID列表
           * @returns {Array} 默认推荐列表
           */
          getDefaultRecommendations(availableMaterials) {
                    // 确保我们只推荐可用的材料
                    const defaultOptions = [
                              {
                                        materialId: 'cet4_001',
                                        id: 'cet4_001', // 同时提供id属性以兼容
                                        title: 'CET4 听力训练 - 校园生活',
                                        difficulty: 'CET4',
                                        match_score: 0.85, // 添加match_score属性
                                        reason: '这是一个基础的四级听力材料，适合初学者'
                              },
                              {
                                        materialId: '2022_06',
                                        id: '2022_06', // 同时提供id属性以兼容
                                        title: '2022年四级听力真题六月第一套',
                                        difficulty: 'CET4',
                                        match_score: 0.8, // 添加match_score属性
                                        reason: '这是最新的四级真题，可以帮助您了解考试形式'
                              },
                              {
                                        materialId: '2022_09',
                                        id: '2022_09', // 同时提供id属性以兼容
                                        title: '2022年四级听力真题九月第一套',
                                        difficulty: 'CET4',
                                        match_score: 0.75, // 添加match_score属性
                                        reason: '这套材料涵盖了多种话题，有助于扩展您的听力范围'
                              },
                              {
                                        materialId: '2022_12_1',
                                        id: '2022_12_1', // 同时提供id属性以兼容
                                        title: '2022年四级听力真题十二月第一套',
                                        difficulty: 'CET4',
                                        match_score: 0.7, // 添加match_score属性
                                        reason: '这套材料包含了多种场景的听力练习'
                              },
                              {
                                        materialId: '2023_06_1',
                                        id: '2023_06_1', // 同时提供id属性以兼容
                                        title: '2023年四级听力真题六月第一套',
                                        difficulty: 'CET4',
                                        match_score: 0.65, // 添加match_score属性
                                        reason: '这是最新的四级真题，难度适中，适合练习'
                              }
                    ];

                    // 过滤出可用的默认推荐
                    if (availableMaterials && availableMaterials.length) {
                              const validDefaults = defaultOptions.filter(
                                        option => availableMaterials.includes(option.materialId)
                              );

                              if (validDefaults.length > 0) {
                                        return validDefaults.slice(0, 3); // 返回前3个
                              }

                              // 如果没有匹配的默认推荐，从可用材料中构建推荐
                              return availableMaterials.slice(0, 3).map(id => ({
                                        materialId: id,
                                        id: id, // 同时提供id属性以兼容
                                        title: `听力材料 - ${id}`,
                                        difficulty: id.includes('cet4') ? 'CET4' : (id.includes('cet6') ? 'CET6' : 'Unknown'),
                                        match_score: 0.6, // 添加match_score属性
                                        reason: '这是系统推荐的基础听力材料'
                              }));
                    }

                    // 如果没有可用材料信息，返回原始默认推荐
                    return defaultOptions.slice(0, 3);
          }
}

// 导出单例实例
export default new RecommendationService(); 