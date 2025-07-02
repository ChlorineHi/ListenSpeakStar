<script>
import MaterialService from '@/services/MaterialService';

export default {
  methods: {
    async viewMaterial(materialId) {
      try {
        // 检查材料是否存在
        // MaterialService可能是一个单例实例而不是类
        const exists = await MaterialService.checkMaterialExists(materialId);
        
        if (exists) {
          // 材料存在，导航到详情页
          this.$router.push(`/listening/${materialId}`);
        } else {
          // 材料不存在，显示提示
          console.error(`材料 ${materialId} 不存在`);
          alert(`抱歉，材料 "${materialId}" 不存在或已被移除。`);
        }
      } catch (error) {
        console.error('检查材料存在性失败:', error);
        // 出错时仍然尝试导航，让详情页处理错误
        this.$router.push(`/listening/${materialId}`);
      }
    }
  }
};
</script> 