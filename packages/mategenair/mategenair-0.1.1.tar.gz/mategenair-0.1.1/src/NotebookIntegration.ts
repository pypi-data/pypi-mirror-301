import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook';
import { CodeCell } from '@jupyterlab/cells';
import { Cell } from '@jupyterlab/cells';
import { ChatbotWidget } from './ChatbotWidget';  // 引入ChatbotWidget

export class NotebookIntegration {
  private tracker!: INotebookTracker;
  private chatbot!: ChatbotWidget;

  constructor(tracker: INotebookTracker, chatbot: ChatbotWidget) {
    if (!tracker) {
      console.error('Notebook tracker is undefined.');
      return;
    }
    
    this.tracker = tracker;
    this.chatbot = chatbot;

    // 监听Notebook的变化，当Notebook切换时为新Notebook添加按钮
    this.tracker.currentChanged.connect(this.onNotebookChanged, this);

    // 监听新的Notebook被添加
    this.tracker.widgetAdded.connect(this.onNotebookAdded, this);
  }

  // 当Notebook发生变化时执行的回调函数
  public onNotebookChanged(): void {
    const notebookPanel = this.tracker.currentWidget;
    if (notebookPanel) {
      this.addButtonsToCells(notebookPanel);
    }
  }

  // 当新Notebook被添加时执行的回调函数
  private onNotebookAdded(tracker: INotebookTracker, notebookPanel: NotebookPanel): void {
    // 等待Notebook完全加载后再添加按钮
    notebookPanel.revealed.then(() => {
      this.addButtonsToCells(notebookPanel);
    });
  }

  // 为每个cell添加按钮
  private addButtonsToCells(notebookPanel: NotebookPanel): void {
    notebookPanel.content.widgets.forEach((cell: Cell) => {
      if (cell instanceof CodeCell) {
        this.addButtonToCell(cell);
      }
    });
  }

  // 向特定的cell添加按钮
  private addButtonToCell(cell: CodeCell): void {
    // 检查是否已经有按钮存在，避免重复添加
    if (cell.node.querySelector('.send-to-chatbot-button')) {
      return;  // 如果按钮已经存在，则直接返回
    }

    const button = document.createElement('button');
    button.textContent = '发送到聊天机器人';
    button.className = 'send-to-chatbot-button';
    button.onclick = () => this.handleButtonClick(cell);
    
    // 默认隐藏按钮
    button.style.display = 'none'; // 使用CSS属性隐藏按钮    
    // 将按钮添加到cell的输出区域
    const outputArea = cell.node.querySelector('.jp-Cell-outputArea');
    if (outputArea) {
      outputArea.appendChild(button);
    }
  }

  // 按钮点击后的处理函数：发送代码和输出到聊天机器人
  private async handleButtonClick(cell: CodeCell): Promise<void> {
    const code = cell.model.sharedModel.getSource();  // 获取cell中的代码
    const output = this.getCellOutput(cell);  // 获取输出内容

    // 将代码和输出发送给聊天机器人
    const userMessage = `代码:\n${code}\n\n输出:\n${output}`;
    await this.chatbot.sendMessageToChatbot(userMessage);
  }

  // 获取cell的输出内容
  private getCellOutput(cell: CodeCell): string {
    const outputs = cell.model.outputs.toJSON();  // 获取cell的输出
    return outputs.map((output: any) => JSON.stringify(output.data)).join('\n') || '无输出';
  }
}
