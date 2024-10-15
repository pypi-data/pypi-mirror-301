// 自动调整文本框高度的函数
export function autoResizeTextarea(textarea: HTMLTextAreaElement): void {
  textarea.style.height = '30px'; // 先重置高度
  textarea.style.height = textarea.value.trim()?`${textarea.scrollHeight}px`:'30px'; // 根据内容调整高度
}

// 复制代码到剪贴板的函数
export function copyCodeToClipboard(codeElement: Element): void {
  const code = codeElement.textContent || '';
  navigator.clipboard.writeText(code)
    .then(() => {
      const button = codeElement.closest('.code-wrapper')?.querySelector('.copy-button') as HTMLButtonElement | null;
      if (button) {
        const originalText = button.textContent || '复制';  // 如果 originalText 为空，默认赋值为 "复制"
        button.innerHTML = '已复制!';  // 使用 innerHTML 强制更新按钮文本

        console.log('Button text updated to: 已复制!');  // 调试信息

        // 强制刷新按钮文本
        button.setAttribute('data-original-text', originalText);  // 将原始文本存储在自定义属性中
        setTimeout(() => {
          button.innerHTML = button.getAttribute('data-original-text') || '复制';  // 恢复到原始文本
          console.log('Button text reverted to: 复制');  // 调试信息
        }, 2000);  // 2秒后恢复原来的文字
      }
    })
    .catch(err => {
      console.error('Failed to copy: ', err);
    });
}
