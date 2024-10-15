import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook';
import { CodeCell } from '@jupyterlab/cells';
import { Cell } from '@jupyterlab/cells';
import { ChatbotWidget } from './ChatbotWidget';  
// import { ApiService } from './ApiService';
// import { KernelMessage } from '@jupyterlab/services';
import { NotebookActions } from '@jupyterlab/notebook';
import { ApiService } from './ApiService';
import { Message } from './types'; // 确保从 types 文件导入 Message

export class SmartProgramming {
  private tracker: INotebookTracker;
  private chatbot: ChatbotWidget;
  // private apiService: ApiService;
  private buttonState:boolean;

  constructor(tracker: INotebookTracker, chatbot: ChatbotWidget) {
    this.tracker = tracker;
    this.chatbot = chatbot;
    // this.apiService = apiService;
    this.buttonState = true;

	  // 监听 cell 添加事件，为新添加的 cell 添加按钮
    this.initOnCellAddedConnect();
  }

  //初始化
  public initDefaultState(callback:Function):void{
    this.onNotebookChanged();
    const notebookPanel = this.tracker.currentWidget;
    if(notebookPanel){
      let smartClassNames=0;
      notebookPanel.content.widgets.map((cell: Cell)=>{
        const hasBtn = cell.node.querySelector('.smart-programming-button')
        if(hasBtn){smartClassNames+=1}
      })
      if(notebookPanel.content.widgets.length===smartClassNames){
        callback()
      }
    }
  }

  // 当 notebook 切换时为新的 notebook 添加按钮
  public onNotebookChanged(): void {
    const notebookPanel = this.tracker.currentWidget;
    this.tracker.currentWidget?.content.model?.cells.changed.connect(this.onCellAdded, this);
    if (notebookPanel) {
      this.addSmartProgrammingButtonToCells(notebookPanel)
    }
  }

  // 监听 cell 添加事件，为新添加的 cell 添加智慧编程按钮
  private onCellAdded(): void {
    const notebookPanel = this.tracker.currentWidget;
    if (notebookPanel) {
      // const cells = notebookPanel.content.widgets;
      // const newCell = cells[cells.length - 1]; // 获取新添加的 cell
      // if (newCell instanceof CodeCell) {
      //   this.debounce(this.addSmartProgrammingButton(newCell),3000);
      // }
      this.addSmartProgrammingButtonToCells(notebookPanel);
    }
  }

  // 当新 notebook 打开时为其 cell 添加按钮
  private onNotebookAdded(sender: INotebookTracker, notebookPanel: NotebookPanel): void {
    if(notebookPanel.revealed){
      notebookPanel.revealed.then(() => {
        this.debounce(this.addSmartProgrammingButtonToCells(notebookPanel),1000);;
      });
    }else{
      this.debounce(this.onNotebookAdded(sender,notebookPanel),3000)
    }
  }

  //关联新增按钮事件
  private initOnCellAddedConnect():void{
    const currentWidget = this.tracker.currentWidget;
    const changed = currentWidget?.content.model?.cells.changed;
    if(currentWidget){
      // 监听 notebook 变化，为新的 notebook 添加按钮
      this.tracker.widgetAdded.connect(this.onNotebookAdded, this);
      this.tracker.currentChanged.connect(this.onNotebookChanged, this);
    }
    if(changed){
      this.tracker.currentWidget?.content.model?.cells.changed.connect(this.onCellAdded, this);
    }else{
      this.debounce(this.initOnCellAddedConnect,2000);
    }
  }

  // 为 notebook 的每个 cell 添加智慧编程按钮
  private addSmartProgrammingButtonToCells(notebookPanel: NotebookPanel): void {
    notebookPanel.content.widgets.forEach((cell: Cell) => {
      if (cell instanceof CodeCell) {
        this.addSmartProgrammingButton(cell);
        this.listenForExecutionErrors(cell); // 新增：监听执行错误
      }
    });
  }

  // 为特定的 cell 添加智慧编程按钮
  // 修改后的 addSmartProgrammingButton 函数
  private addSmartProgrammingButton(cell: CodeCell): void {    
    // 防止重复添加按钮
    const addSmartProgrammingButton = cell.node.querySelector('.smart-programming-button')
    if (addSmartProgrammingButton) {
      return;
    }

    const button = document.createElement('button');
    button.className = 'smart-programming-button';
    // button.onclick = () => this.openInputPopup(cell, button);  // 调整弹窗的位置到按钮的右侧

    // 添加弹窗
    button.onclick = () => {
      //校验用户是否登录
      this.checkLoginStatusOnLoad(()=>{
        const existingPopup = cell.node.querySelector('.smart-popup');
        if (existingPopup) {
          existingPopup.remove();  // 如果弹窗已存在，点击时关闭
        } else {
          this.showButtonsBelowCell(cell);  // 显示新的弹窗
        }
      },()=>{
        this.debounce(this.messageWaring("登录MateGen Air，开启智慧编程",cell),3000)
      })
    };
    // 尝试将按钮插入到输入区域
    // const inputArea = cell.node.querySelector('.jp-Cell-inputWrapper');  // 找到输入区
    // if (inputArea) {
    //   inputArea.appendChild(button);  // 将按钮插入输入区的底部或右侧
    // } else {
    //   console.warn('Input area not found for this cell.');
    // }
    // 封装检查输入区域的逻辑
    const checkInputArea = () => {
      const inputArea = cell.node.querySelector('.jp-Cell-inputWrapper');  // 找到输入区
      if (inputArea) {
        const tempClassName = cell.node.querySelector('.smart-programming-button')
        !tempClassName?inputArea.appendChild(button):null;  // 将按钮插入输入区的底部或右侧
      } else {
        console.warn('Input area not found for this cell.');
      }
    };
    // 使用 setTimeout 延时，确保 DOM 元素已加载
    setTimeout(checkInputArea, 100);
	}    

  // 检查 JWT 是否过期
  private isTokenExpired(token: string): boolean {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiry = payload.exp * 1000; // 转换为毫秒
      return Date.now() > expiry;
  }

  //显示提示
  private messageWaring(msg:string,cell:CodeCell):void{
    const tempId = "msgDivId_"+Math.random();
    const checkLogin = () => {
      const parentNode = cell.node.querySelector('.jp-Cell-outputWrapper') as HTMLDivElement;  // 找到输入区
      if (parentNode) {
        const msgDiv = document.createElement('div');
        msgDiv.id=tempId;
        msgDiv.classList.add("chat-message-box")
        msgDiv.innerHTML=`<span style="color:#fff">${msg}</span>`;
        parentNode.appendChild(msgDiv);
        setTimeout(()=>{
          const tempMsgDiv = document.getElementById(tempId);
          tempMsgDiv?.remove();
        },3000)
      } else {
        // console.warn('Input area not found for this cell.');
      }
    };
    // 使用 setTimeout 延时，确保 DOM 元素已加载
    setTimeout(checkLogin, 100);    
  }

  private showButtonsBelowCell(cell: CodeCell): void {
    // 先移除已经存在的按钮区域，防止重复添加
    const existingButtons = cell.node.querySelector('.smart-buttons');
    if (existingButtons) {
      existingButtons.remove();
      return;
    }

    // 创建按钮容器
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'smart-buttons'; // 可以在CSS中定义样式
    buttonContainer.style.display = 'flex';
    buttonContainer.style.justifyContent = 'flex-start'; // 按钮左对齐
    buttonContainer.style.marginTop = '5px';
    buttonContainer.style.marginLeft = '70px'; // 整体右移 70px，根据需要调整

    // 创建每个按钮
    const buttons = [
      { text: 'AI自动编程', action: () => this.openInputPopup(cell) },
      { 
        text: '逐行代码解释', 
        action: () => {
        const cellContent = cell.model.sharedModel.getSource();  // 获取当前 cell 的内容
        const userMessage = `请将以下代码进行逐行注释:\n${cellContent}`;  // 添加前缀
        this.sendToChatbotWithAnnotation(userMessage, cell);  // 调用 sendToChatbot 函数    		
          } 
        },
      { 
        text: '开启代码会话', 
        action: async () => {
          const cellContent = cell.model.sharedModel.getSource();  // 获取当前 cell 的内容
          await this.chatbot.sendMessageToChatbot(`你好，请帮我仔细解释下这段代码的含义:\n${cellContent}`);
          } 
        }
    ];

    buttons.forEach(buttonInfo => {
      const button = document.createElement('button');
      button.textContent = buttonInfo.text;
      button.style.padding = '5px 10px'; // 按钮样式
      button.style.margin = '0 5px';
      button.style.cursor = 'pointer';

      // 点击事件，触发功能并隐藏按钮区域
      button.addEventListener('click', () => {
        buttonInfo.action();
        buttonContainer.remove(); // 点击后移除按钮区域
      });

    // 将按钮添加到容器中
    buttonContainer.appendChild(button);
  });

  // 将按钮容器插入到 cell 的输出区域下方
  const outputArea = cell.node.querySelector('.jp-Cell-outputArea');
  if (outputArea) {
    outputArea.appendChild(buttonContainer);
  } else {
    // 如果输出区域不存在，可以将按钮插入到其他合适的位置
    cell.node.appendChild(buttonContainer);
  }
}


// 打开输入弹窗，用户可以在弹窗中输入内容
private openInputPopup(cell: CodeCell): void {
  // 如果已经有弹窗存在，直接关闭现有的弹窗
  const existingPopup = document.querySelector('.input-popup');
  if (existingPopup) {
    existingPopup.remove();
    return;
  }

  // 创建输入框的弹窗容器
  const popup = document.createElement('div');
  popup.className = 'input-popup';
  
  // 创建多行输入框，允许用户换行输入
  const inputField = document.createElement('textarea');
  inputField.placeholder = '输入编程需求，开启自动编程...';
  inputField.rows = 1;  // 设置默认行数
  inputField.style.resize = 'none';  // 禁用手动调整大小
  inputField.className = 'input-field';  // 设置类名方便样式控制

  // 当用户按下 Enter 时发送消息
  inputField.addEventListener('keydown', (event) => {
    // 如果按下的是 Enter 且未按 Shift
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();  // 阻止默认的换行行为
      const userMessage = inputField.value.trim();
      if (userMessage) {
        // 将用户输入显示在 cell 上方，并发送给机器人
        this.displayUserInputAboveCell(cell, userMessage);
        
        this.sendToChatbot(userMessage, cell);  // 发送消息给聊天机器人
      }
      popup.remove();  // 发送后移除输入框
    }
  });

  // 当用户按下 Esc 时，关闭输入框
  inputField.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      popup.remove();
    }
  });

  // 将输入框添加到弹窗中
  popup.appendChild(inputField);
  
  // 将弹出框插入到 cell 的 DOM 节点内
  cell.node.appendChild(popup);


  // 自动聚焦到输入框
  inputField.focus();
}


  // 将用户输入显示在 cell 上方
  private displayUserInputAboveCell(cell: CodeCell, message: string): void {
    const userMessageDiv = document.createElement('div');
    userMessageDiv.textContent = `编程提示: ${message}`;
    userMessageDiv.className = 'user-message-display';

    // 将用户输入的消息显示在 cell 上方
    const cellNode = cell.node;
    cellNode.parentNode?.insertBefore(userMessageDiv, cellNode);
  }
  
	private extractPythonCode(reply: string): string {
	  const codeBlockRegex = /```python([\s\S]*?)```/g;
	  const matches = reply.match(codeBlockRegex);
	  
	  if (matches) {
	    // 提取所有 Python 代码块
	    return matches.map(match => match.replace(/```python|```/g, '').trim()).join('\n');
	  }
	  return '';  // 如果没有 Python 代码则返回空字符串
	}
	
	// 然后在 sendToChatbot 函数中使用这个提取代码的逻辑
	private async sendToChatbot(userMessage: string, cell: CodeCell): Promise<void> {
		const apiService = new ApiService();
		
       // 添加动态等待效果
       let dotCount = 1;
       const waitingMessage = 'MateGen正在编写代码，请稍后';
       cell.model.sharedModel.setSource(`${waitingMessage}...`);

         // 用于更新等待中的点数（1到3个点）
        const intervalId = setInterval(() => {
          const dots = '.'.repeat(dotCount);
          cell.model.sharedModel.setSource(`${waitingMessage}${dots}`);
          dotCount = dotCount % 3 + 1;  // 循环更新点数
        }, 500);  // 每500ms更新一次点
		
	  try {
	    // 将 userMessage 转换为 { role: 'user', content: userMessage } 格式
	    const messageObject: Message = { role: 'user', content: userMessage };
	    
	    // 调用 ApiService 的 getBotReplyNoStream 方法，并传递消息对象数组
	    const botReply = await apiService.getBotReplyNoStream([messageObject]);
	    // const botReply = await this.chatbot.sendMessageToChatbot(userMessage);
	    
          // 停止动态等待效果
          clearInterval(intervalId);	
          
	    // 提取 Python 代码
	    const pythonCode = this.extractPythonCode(botReply);
	    
          // 在插入大模型生成的代码前，清空之前的等待提示
          cell.model.sharedModel.setSource(''); // 清空 cell 的内容	
          
	    if (pythonCode) {
	      // 将 Python 代码插入到当前 cell 中
	      const currentCode = cell.model.sharedModel.getSource();
	      const newCode = `# 以下代码由MateGen编写，请审查后使用:\n${pythonCode}`;
	      
	      // 逐字输出新生成的代码
	      this.printCodeToCellGradually(cell, newCode, currentCode);
	    } else {
	      console.log('没有提取到 Python 代码');
	    }
	  } catch (error) {
	    console.error('发送消息到聊天机器人时发生错误:', error);
	  }
	}
	
// 代码注释函数
public async sendToChatbotWithAnnotation(userMessage: string, cell: CodeCell): Promise<void> {
  const apiService = new ApiService();

  // 获取原始的代码内容
  const originalContent = cell.model.sharedModel.getSource();

  // 添加滚动的“正在编写注释...”提示
  let dotCount = 1;
  const waitingMessage = 'MateGen正在编写注释，请稍后';
  const annotationMessage = `${waitingMessage}...`;
  cell.model.sharedModel.setSource(`${annotationMessage}\n${originalContent}`);

  // 用于更新滚动中的点数（1到3个点）
  const intervalId = setInterval(() => {
    const dots = '.'.repeat(dotCount);
    cell.model.sharedModel.setSource(`${waitingMessage}${dots}\n${originalContent}`);
    dotCount = dotCount % 3 + 1;  // 循环更新点数
  }, 500);  // 每500ms 更新一次点

  try {
    // 将 userMessage 转换为 { role: 'user', content: userMessage } 格式
    const messageObject: Message = { role: 'user', content: userMessage };
    
    // 调用 ApiService 的 getBotReplyNoStream 方法，并传递消息对象数组
    const botReply = await apiService.getBotReplyNoStream([messageObject]);

    // 停止动态等待效果
    clearInterval(intervalId);

	const pythonCode = this.extractPythonCode(botReply);
	const newContent = `# 以下代码的注释由MateGen生成:\n${pythonCode}`;
	
    // 替换 cell 中的内容，去掉等待信息，并将大模型返回的内容放入
    cell.model.sharedModel.setSource(newContent);  // 一次性替换原内容
  } catch (error) {
    // 停止动态等待效果
    clearInterval(intervalId);
    console.error('获取逐行注释时发生错误:', error);
  }
}

	
	// 逐字将代码打印到 cell 中
	private printCodeToCellGradually(cell: CodeCell, code: string, currentCode: string): void {
	  let index = 0;
	  
	  const printNextCharacter = () => {
	    if (index < code.length) {
	      const newText = currentCode + code.slice(0, index + 1);
	      cell.model.sharedModel.setSource(newText);  // 每次更新 cell 的内容
	      index++;
	      
	      // 递归调用，间隔一定时间输出下一个字符
	      setTimeout(printNextCharacter, 10);  // 每个字符间隔10ms，可以根据需要调整速度
	    }
	  };
	
	  // 开始逐字打印
	  printNextCharacter();
	}
	
  // 新增：监听代码单元执行结果并检测错误
  private async listenForExecutionErrors(cell: CodeCell): Promise<any> {
    const future = cell.outputArea.future;
    if (future) {
      // console.log('监听代码单元的执行');
      const msg:any = await future.done.then(res=>res);
      // console.log('执行结果:', msg);
      if (msg.content.status === 'error') {
        this.debounce(this.addFixButtonToCell(cell, msg.content),3000);  // 如果有错误，添加修复按钮
      }
    	
      // this.addFixButtonToCell(cell,future.msg.content);  // 如果有错误，添加修复按钮
      // future.onReply = (msg) => {
      // 	console.log('执行结果:', msg);
      //   if (msg.content.status === 'error') {
      //     this.addFixButtonToCell(cell, msg.content);  // 如果有错误，添加修复按钮
      //   }
      // };
    }
  }

  // 新增：为出现错误的 cell 添加修复按钮
  private addFixButtonToCell(cell: CodeCell, errorMsg: any): void {
    // 防止重复添加按钮
    const fixCodeButton = cell.node.querySelector('.fix-code-button')
    if (fixCodeButton) {
      return;
    }
    
    const fixButton = document.createElement('button');
    fixButton.className = 'fix-code-button';
    fixButton.textContent = '修复代码';

    // 按钮点击事件，发送代码和错误信息到 Chatbot
    fixButton.onclick = () => {
      const code = cell.model.sharedModel.getSource();  // 获取当前 cell 的代码
      const errorMessage = errorMsg.evalue || '未知错误';  // 获取错误信息

      //校验用户是否登录
      this.checkLoginStatusOnLoad(()=>{
        //控制按钮点击频率
        if(this.buttonState){
          this.buttonState=false;//按钮已经点击过限制按钮点击
          this.sendToChatbotWithError(code, errorMessage, cell);  // 发送到大模型进行修复
        }
      },()=>{
        this.debounce(this.messageWaring("登录MateGen Air，开启智慧编程",cell),3000)
      })
    };

    // 延迟插入按钮，确保输出区域已经渲染
    setTimeout(() => {
      const outputArea = cell.node.querySelector('.jp-OutputArea-output');
      if (outputArea) {
        const tempFixCodeBuutton = cell.node.querySelector('.fix-code-button')
        !tempFixCodeBuutton?outputArea.appendChild(fixButton):null;  // 将按钮插入到输出区域
      }
    }, 500);  // 延迟1000ms等待输出区域渲染
  }

  //校验用户是否登录
  private checkLoginStatusOnLoad(successCallback:Function,errorCallback:Function):void{
    const token = localStorage.getItem('auth_token');
    if (token && !this.isTokenExpired(token)) {
      successCallback()
    }else{
      errorCallback()
    }
  }

  // 修改后的 sendToChatbot 函数，支持发送错误信息
  private async sendToChatbotWithError(code: string, errorMessage: string, cell: CodeCell): Promise<void> {
    // 添加动态等待效果
    let dotCount = 1;
    const waitingMessage = '# MateGen正在修复代码';
    cell.model.sharedModel.setSource(`${waitingMessage}...`);

    // 更新等待中的点数
    const intervalId = setInterval(() => {
      const dots = '.'.repeat(dotCount);
      cell.model.sharedModel.setSource(`${waitingMessage}${dots}`);
      dotCount = dotCount % 3 + 1;
    }, 500);

    try {
      const botReply = await this.chatbot.sendMessageToChatbot(`以下代码出现错误:\n${code}\n错误信息:\n${errorMessage}`);

      // 停止动态等待效果
      clearInterval(intervalId);

      // 提取 Python 代码
      const pythonCode = this.extractPythonCode(botReply);

      // 在插入大模型生成的代码前，设置之前的等待提示
      cell.model.sharedModel.setSource(code);

      if (pythonCode) {
        this.insertCodeIntoNewCell(pythonCode);  // 将修复后的代码插入新的代码单元
      } else {
        console.log('没有提取到 Python 代码');
      }
      this.buttonState=true;//取消限制按钮点击
    } catch (error) {
      console.error('发送消息到聊天机器人时发生错误:', error);
      this.buttonState=true;//取消限制按钮点击
    }
  }

  // 将修复代码插入到新的代码单元
  private insertCodeIntoNewCell(code: string): void {
    const notebookPanel = this.tracker.currentWidget;

    if (notebookPanel && notebookPanel.content && notebookPanel.model) {
      // 插入一个新单元格
      NotebookActions.insertBelow(notebookPanel.content);

      // 获取最后插入的单元格
      const newCell = notebookPanel.content.widgets[notebookPanel.content.widgets.length - 1] as CodeCell;

      // 设置新单元格的内容为修复后的代码
      newCell.model.sharedModel.setSource(code);
    }
  }


  //防抖函数
  private debounce(fn:any, wait:number) {
      let timeout:any = null;
      return () => {
          let context = this;
          let args = arguments;
          if (timeout) clearTimeout(timeout);
          let callNow = !timeout;
          timeout = setTimeout(() => {
              timeout = null;
          }, wait);
          if (callNow) fn.apply(context, args);
      };
  }


}
