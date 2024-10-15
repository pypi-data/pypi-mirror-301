import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ICommandPalette,
  MainAreaWidget
} from '@jupyterlab/apputils';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ChatbotWidget } from './ChatbotWidget';  // 从拆分后的模块中导入 ChatbotWidget
import { INotebookTracker } from '@jupyterlab/notebook';
import { ILauncher } from '@jupyterlab/launcher';  // 引入 ILauncher 模块
import { LabIcon } from '@jupyterlab/ui-components';
import chatbotSvg from '../style/image/chatbot-icon.svg';  // 引入自定义 SVG 图标

// 创建一个 LabIcon 实例，使用你自己的 SVG 图标
const chatbotIcon = new LabIcon({
  name: 'chatbot-icon',
  svgstr: chatbotSvg
});

// 插件的激活函数
function activate(app: JupyterFrontEnd, palette: ICommandPalette, tracker: INotebookTracker, settingRegistry: ISettingRegistry | null, launcher: ILauncher | null) {
  console.log('MateGen Air is activated!');

  let widget: MainAreaWidget<ChatbotWidget>;

  // 检查Notebook tracker是否存在
  if (!tracker) {
    console.error('Notebook tracker is undefined. Plugin cannot activate.');
    return;
  }

  // 定义一个命令用于启动聊天机器人
  const command: string = 'chatbot:open1';
  app.commands.addCommand(command, {
    label: '启动MateGen Air',
    icon: chatbotIcon,  // 设置图标
    execute: () => {
      // 检查当前Notebook是否存在
      // const notebook = tracker.currentWidget;
      // if (!notebook) {
        // console.warn('No active notebook found. Cannot open chatbot.');
        // return;
      // }

      if (!widget || widget.isDisposed) {
        const content = new ChatbotWidget(tracker, app.serviceManager.contents);  // 传入tracker和contents到ChatbotWidget
        widget = new MainAreaWidget({ content });
        widget.id = 'chatbot-jupyterlab1';
        widget.title.label = 'MateGen Air';
        widget.title.closable = true;
      }

      // 如果窗口没有附加到shell，则添加
      if (!widget.isAttached) {
        app.shell.add(widget, 'main');
      }
      // 激活窗口
      app.shell.activateById(widget.id);
    }
  });

  // 将命令添加到命令面板
  palette.addItem({ command, category: '工具' });

  // 如果launcher可用，添加启动图标
  if (launcher) {
    launcher.add({
      command: command,  // 指定启动命令
      category: '工具',  // 图标分类
      rank: 1            // 排序优先级
    });
  }  
  
  // 加载插件设置（如果存在）
  if (settingRegistry) {
    settingRegistry
      .load(plugin.id)
      .then(settings => {
        console.log('chatbot settings loaded:', settings.composite);
      })
      .catch(reason => {
        console.error('Failed to load settings for chatbot.', reason);
      });
  }
}

// 定义插件对象
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'chatbot1',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker],  // 添加INotebookTracker作为必需项
  optional: [ISettingRegistry, ILauncher],        // 将ILauncher添加为可选项
  activate: activate
};

// 导出插件
export default plugin;
