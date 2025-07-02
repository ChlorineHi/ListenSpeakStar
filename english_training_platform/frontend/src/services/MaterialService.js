/**
 * 材料服务 - 用于获取和处理听力材料数据
 */
class MaterialService {
          /**
           * 获取材料索引，包含所有难度级别和材料概览
           * @returns {Promise<Object>} 材料索引数据
           */
          async getMaterialsIndex() {
                    try {
                              const response = await fetch('/materials/index.json');
                              if (!response.ok) {
                                        throw new Error('无法获取材料索引');
                              }
                              return await response.json();
                    } catch (error) {
                              console.error('获取材料索引失败:', error);
                              throw error;
                    }
          }

          /**
           * 获取指定难度级别的所有材料
           * @param {string} difficulty 难度级别 (CET4, CET6, IELTS, TOEFL)
           * @returns {Promise<Array>} 材料列表
           */
          async getMaterialsByDifficulty(difficulty) {
                    try {
                              const index = await this.getMaterialsIndex();
                              const difficultyInfo = index.difficulties.find(d => d.id === difficulty);

                              if (!difficultyInfo) {
                                        throw new Error(`找不到难度级别: ${difficulty}`);
                              }

                              const response = await fetch(difficultyInfo.materials_path);
                              if (!response.ok) {
                                        throw new Error(`无法获取${difficulty}材料`);
                              }

                              const data = await response.json();
                              return data.materials;
                    } catch (error) {
                              console.error(`获取${difficulty}材料失败:`, error);
                              throw error;
                    }
          }

          /**
           * 标准化材料ID，处理不同格式的ID
           * @param {string} materialId 原始材料ID
           * @returns {string} 标准化后的ID
           */
          normalizeId(materialId) {
                    // 处理特殊格式的ID，如2022_12_01 -> 2022_12_1
                    const idParts = materialId.split('_');
                    if (idParts.length >= 3) {
                              const lastPart = idParts[2];
                              if (lastPart === '01') {
                                        return `${idParts[0]}_${idParts[1]}_1`;
                              } else if (lastPart === '02') {
                                        return `${idParts[0]}_${idParts[1]}_2`;
                              }
                    }
                    return materialId;
          }

          /**
           * 检查材料ID是否存在于可用材料列表中
           * @param {string} materialId 材料ID
           * @returns {Promise<boolean>} 是否存在
           */
          async checkMaterialExists(materialId) {
                    try {
                              // 获取index.json中的可用材料列表
                              const response = await fetch('/materials/index.json');
                              if (!response.ok) {
                                        console.error('无法获取材料索引');
                                        return false;
                              }

                              const indexData = await response.json();

                              // 检查材料ID是否在可用材料列表中
                              if (indexData.available_materials && indexData.available_materials.includes(materialId)) {
                                        return true;
                              }

                              // 如果不在可用列表中，再检查materials_details
                              if (indexData.materials_details) {
                                        const exists = indexData.materials_details.some(material => material.id === materialId);
                                        if (exists) {
                                                  return true;
                                        }
                              }

                              console.warn(`材料ID "${materialId}" 不在可用材料列表中`);
                              return false;
                    } catch (error) {
                              console.error('检查材料存在性时出错:', error);
                              return false;
                    }
          }

          /**
           * 获取材料详情（包含标签信息）
           * @param {string} materialId 材料ID
           * @returns {Promise<Object>} 材料详情
           */
          async getMaterialDetails(materialId) {
                    try {
                              // 获取index.json中的材料详情
                              const response = await fetch('/materials/index.json');
                              if (!response.ok) {
                                        console.error('无法获取材料索引');
                                        return null;
                              }

                              const indexData = await response.json();

                              // 查找匹配的材料详情
                              if (indexData.materials_details) {
                                        const materialDetail = indexData.materials_details.find(material => material.id === materialId);
                                        if (materialDetail) {
                                                  return materialDetail;
                                        }
                              }

                              console.warn(`未找到材料ID "${materialId}" 的详细信息`);
                              return null;
                    } catch (error) {
                              console.error('获取材料详情时出错:', error);
                              return null;
                    }
          }

          /**
           * 获取指定ID的材料详情
           * @param {string} materialId 材料ID
           * @returns {Promise<Object>} 材料详情
           */
          async getMaterialById(materialId) {
                    // 先检查材料是否存在
                    const exists = await this.checkMaterialExists(materialId);
                    if (!exists) {
                              console.error(`材料ID "${materialId}" 不存在，无法获取`);
                              throw new Error(`无法获取材料: ${materialId} (材料不存在)`);
                    }

                    try {
                              console.log(`开始获取材料: ${materialId}`);

                              // 标准化ID，处理特殊格式
                              const normalizedId = this.normalizeId(materialId);
                              if (normalizedId !== materialId) {
                                        console.log(`ID已标准化: ${materialId} -> ${normalizedId}`);
                              }

                              // 从ID中提取难度级别前缀
                              const idParts = normalizedId.split('_');
                              const difficultyPrefix = idParts[0].toUpperCase();
                              let difficulty;
                              let directoryName = normalizedId; // 使用标准化后的ID作为默认目录名

                              // 映射前缀到难度级别
                              switch (difficultyPrefix) {
                                        case 'CET4':
                                                  difficulty = 'CET4';
                                                  break;
                                        case 'CET6':
                                                  difficulty = 'CET6';
                                                  break;
                                        case 'IELTS':
                                                  difficulty = 'IELTS';
                                                  break;
                                        case 'TOEFL':
                                                  difficulty = 'TOEFL';
                                                  break;
                                        case '2022':
                                        case '2023':
                                                  // 对于年份格式的ID，使用完整ID作为目录路径
                                                  difficulty = normalizedId;
                                                  break;
                                        default:
                                                  // 如果无法确定难度，尝试从索引中查找
                                                  try {
                                                            const index = await this.getMaterialsIndex();
                                                            const latestMaterial = index.latest_materials.find(m => m.id === materialId);
                                                            if (latestMaterial) {
                                                                      difficulty = latestMaterial.difficulty;
                                                                      console.log(`从索引中找到材料难度: ${difficulty}`);
                                                            } else {
                                                                      console.warn(`无法从ID确定难度，使用默认难度: CET4`);
                                                                      difficulty = 'CET4';
                                                            }
                                                  } catch (e) {
                                                            console.warn(`获取索引失败，使用默认难度: CET4`);
                                                            difficulty = 'CET4';
                                                  }
                              }

                              // 首先尝试从本地材料文件获取（更可靠）
                              let materialsPath = `/materials/${difficulty}/materials.json`;
                              console.log(`尝试从本地文件获取: ${materialsPath}`);

                              try {
                                        let response = await fetch(materialsPath);

                                        // 如果找不到完全匹配的目录，尝试其他可能的格式
                                        if (!response.ok && idParts.length >= 3) {
                                                  console.log(`无法从 ${difficulty} 获取材料，尝试其他可能的目录名格式`);

                                                  // 尝试直接使用ID作为目录
                                                  materialsPath = `/materials/${normalizedId}/materials.json`;
                                                  response = await fetch(materialsPath);

                                                  if (response.ok) {
                                                            directoryName = normalizedId;
                                                            console.log(`找到有效路径: ${materialsPath}`);
                                                  } else {
                                                            // 尝试不同的目录名格式
                                                            const possibleDirectoryNames = [
                                                                      `${idParts[0]}_${idParts[1]}_${idParts[2]}`, // 原始格式
                                                                      `${idParts[0]}_${idParts[1]}`, // 例如：2022_12
                                                                      `${idParts[0]}_${idParts[1]}_1`, // 例如：2022_12_1
                                                                      `${idParts[0]}_${idParts[1]}_2`  // 例如：2022_12_2
                                                            ];

                                                            for (const dirName of possibleDirectoryNames) {
                                                                      if (dirName === directoryName) continue; // 跳过已尝试过的

                                                                      console.log(`尝试从其他可能的目录获取: ${dirName}`);
                                                                      materialsPath = `/materials/${dirName}/materials.json`;
                                                                      response = await fetch(materialsPath);
                                                                      if (response.ok) {
                                                                                directoryName = dirName;
                                                                                console.log(`找到有效路径: ${materialsPath}`);
                                                                                break;
                                                                      }
                                                            }
                                                  }
                                        }

                                        if (response.ok) {
                                                  const data = await response.json();
                                                  let material;

                                                  if (Array.isArray(data)) {
                                                            material = data.find(m => m.id === materialId || m.id === normalizedId);
                                                  } else if (data.materials && Array.isArray(data.materials)) {
                                                            material = data.materials.find(m => m.id === materialId || m.id === normalizedId);
                                                  }

                                                  if (material) {
                                                            // 添加完整的音频URL路径
                                                            if (material.audio_file && !material.audio_url) {
                                                                      material.audio_url = `/materials/${directoryName}/${material.audio_file}`;
                                                                      console.log(`设置音频URL: ${material.audio_url}`);
                                                            }

                                                            console.log(`成功从本地文件获取材料: ${materialId}`);
                                                            return material;
                                                  }
                                        }

                                        console.log(`从本地文件未找到材料，尝试从API获取`);
                              } catch (fileError) {
                                        console.warn('从本地文件获取材料失败，尝试从API获取:', fileError);
                              }

                              // 如果本地文件获取失败，尝试从API获取材料
                              try {
                                        const apiUrl = `http://localhost:5000/api/listening/material/${materialId}`;
                                        console.log(`尝试从API获取: ${apiUrl}`);

                                        const response = await fetch(apiUrl);

                                        // 检查响应类型，确保是JSON
                                        const contentType = response.headers.get('content-type');
                                        if (!contentType || !contentType.includes('application/json')) {
                                                  console.error(`API返回了非JSON响应: ${contentType}`);
                                                  throw new Error('API返回了非JSON响应');
                                        }

                                        if (response.ok) {
                                                  const material = await response.json();
                                                  if (material && material.id) {
                                                            // 确保audio_url是完整路径
                                                            if (material.audio_file && !material.audio_url) {
                                                                      material.audio_url = `/materials/${directoryName}/${material.audio_file}`;
                                                            }
                                                            console.log(`从API成功获取材料: ${materialId}`);
                                                            return material;
                                                  } else {
                                                            console.error('API返回的材料数据无效');
                                                            throw new Error('无效的材料数据');
                                                  }
                                        } else {
                                                  console.error(`API返回错误状态码: ${response.status}`);
                                                  throw new Error(`API请求失败: ${response.status}`);
                                        }
                              } catch (apiError) {
                                        console.error('从API获取材料失败:', apiError);
                                        throw new Error(`无法获取材料: ${materialId}`);
                              }
                    } catch (error) {
                              console.error(`获取材料详情失败:`, error);
                              throw error;
                    }
          }

          /**
           * 获取按主题筛选的材料
           * @param {string} topic 主题
           * @returns {Promise<Array>} 材料列表
           */
          async getMaterialsByTopic(topic) {
                    try {
                              const index = await this.getMaterialsIndex();
                              const result = [];

                              // 遍历所有难度级别
                              for (const difficulty of index.difficulties) {
                                        const response = await fetch(difficulty.materials_path);
                                        if (!response.ok) continue;

                                        const data = await response.json();

                                        // 筛选包含指定主题的材料
                                        const filteredMaterials = data.materials.filter(material =>
                                                  material.topics && material.topics.includes(topic)
                                        );

                                        result.push(...filteredMaterials);
                              }

                              return result;
                    } catch (error) {
                              console.error(`按主题获取材料失败:`, error);
                              throw error;
                    }
          }

          /**
           * 获取最新的材料列表
           * @param {number} limit 限制返回的材料数量
           * @returns {Promise<Array>} 材料列表
           */
          async getLatestMaterials(limit = 5) {
                    try {
                              const index = await this.getMaterialsIndex();
                              return index.latest_materials.slice(0, limit);
                    } catch (error) {
                              console.error('获取最新材料失败:', error);
                              throw error;
                    }
          }

          /**
           * 获取所有可用的主题
           * @returns {Promise<Array>} 主题列表
           */
          async getAllTopics() {
                    try {
                              const index = await this.getMaterialsIndex();
                              return index.topics;
                    } catch (error) {
                              console.error('获取主题列表失败:', error);
                              throw error;
                    }
          }
}

// 导出单例实例
export default new MaterialService(); 