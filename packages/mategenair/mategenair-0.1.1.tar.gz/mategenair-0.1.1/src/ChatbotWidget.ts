import { Widget } from '@lumino/widgets';
import { marked } from 'marked';
import { markedHighlight } from 'marked-highlight';
import DOMPurify from 'dompurify';
import * as Prism from 'prismjs';
import { autoResizeTextarea, copyCodeToClipboard } from './UIHelper';
import { SessionManager } from './SessionManager';
import { Session, Message, PorjectItemInterface, formatStringInterface } from './types'; // 确保从 types 文件导入 Message
import { ApiService } from './ApiService';
import { LoginManager } from './LoginManager';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-css';
import 'prismjs/themes/prism-okaidia.css';
import { Contents } from '@jupyterlab/services'; // 使用 IManager 来管理文件
import { INotebookTracker } from '@jupyterlab/notebook';
import { NotebookIntegration } from './NotebookIntegration'; // 引入Jupyter交互模块
import { SmartProgramming } from './SmartProgramming'; // 引入智慧编程模块
import OpenAI from "openai";
declare interface document{
  selection:any
}

export class ChatbotWidget extends Widget {
  private readonly MAX_CONTEXT_MESSAGES = 50;
  private notebookIntegration: NotebookIntegration; // 新增发送代码功能
  private smartProgramming: SmartProgramming; // 新增智慧编程集成
  private sessionManager: SessionManager;
  private apiService: ApiService;
  private mateGenApiKey: string;  // 用于存储 MateGen API Key
  private decryptedApiKey: string | null = null; // 新增变量存储解密后的API Key  
  private currentSession: Session | null = null;
  private timer: any;
  private publicPorjectData: Array<PorjectItemInterface>;
  private useFetchPorjectData: Array<PorjectItemInterface>;

  // MateGen相关
  private contents: Contents.IManager;
  private readonly LOG_FILE = 'assistant_log.log'; // 存储在根目录下的日志文件名
  private readonly KNOWLEDGE_BASE_FILE = 'knowledgeBase.log'; // 知识库日志文件名
  private readonly KNOWLEDGE_BASE_FOLDER = 'knowledge_base'; // 知识库文件夹名
  private assistantId: string | null = null; // 当前assistant_id
  private encryptedApiKey: string | null = null; // 当前assistant_id

  // DOM 元素
  private chatLog!: HTMLDivElement;
  private input!: HTMLTextAreaElement;
  private button!: HTMLButtonElement;
  private toggleSidebarTopButton!: HTMLButtonElement;
  private toggleSidebarLeftButton!: HTMLButtonElement;
  private newChatButton!: HTMLButtonElement;
  private newChatLeftButton!: HTMLButtonElement;
  private sessionList!: HTMLDivElement;
  private sidebar!: HTMLDivElement;
  private loginManager!: LoginManager;
  private chatContainer!: HTMLDivElement;
  private loginContainer!: HTMLDivElement;
  private toggleTitle!: HTMLDivElement;
  private toggleSidebarBg!: HTMLDivElement;
  private chatbotDefaultEdit!: HTMLDivElement;
  private chatbotDefaultResponse!: HTMLDivElement;
  private chatLogDefaultContent!: HTMLDivElement;
  private logout!: HTMLLIElement;
  private btnReset!: HTMLButtonElement;
  private selectValue!: HTMLSelectElement;
  private typeNameClick!: HTMLDivElement;
  private popupFooterDesc!: HTMLDivElement;
  private knowledgeStatusElement!: HTMLDivElement;
  private popupHeadSelectGroup!: HTMLDivElement;
  private selectBody!: HTMLDivElement;
  private popupSelectBox!: HTMLDivElement;

  // MateGen DOM元素
  private apiKeyModal!: HTMLDivElement;
  private apiKeyInput!: HTMLInputElement;
  private apiKeyVerifyButton!: HTMLButtonElement;
  private apiKeyConfirmButton!: HTMLButtonElement;
  private apiKeyCancelButton!: HTMLButtonElement;
  private apiKeyResetButton!: HTMLButtonElement;

  constructor(tracker: INotebookTracker, contents: Contents.IManager, mateGenApiKey: string = '') {
    super();
    this.addClass('jp-ChatbotWidget');
    this.sessionManager = new SessionManager(contents); // 使用 Contents.IManager
    this.mateGenApiKey = mateGenApiKey;
    this.apiService = new ApiService(mateGenApiKey);        
    this.contents = contents;
    this.assistantId = this.assistantId;
    this.encryptedApiKey = this.encryptedApiKey;
    this.checkOrCreateLogFile();    
    this.checkOrCreateKnowledgeBaseFileAndFolder();
    this.timer = null;
    clearInterval(this.timer);

    this.initializeDOM();

    // MateGen相关
    this.bindHeaderLogoClickEvent();
    
    //初始化默认会话内容
    this.initDefaultChatLog();
    this.bindEventHandlers();
    this.initializeLoginManager();
    this.configureMarked();
    this.loadSessions(); // 加载历史会话
    // 初始化Notebook集成
    this.notebookIntegration = new NotebookIntegration(tracker, this);

    // 初始化智慧编程集成
    this.smartProgramming = new SmartProgramming(tracker, this);

    // 手动触发一次Notebook的变化，确保为当前Notebook添加按钮
    this.notebookIntegration.onNotebookChanged();
    this.smartProgramming.onNotebookChanged(); // 触发智慧编程的按钮添加

    this.timer = setInterval(() => {
      this.notebookIntegration.onNotebookChanged();
      // console.log("初始u对话框---------")
      this.smartProgramming.initDefaultState(() => {
        // clearInterval(this.timer);
        // this.timer=null;
        // console.log("初始u对话框初始u对话框初始u对话框",this.timer)
      })
    }, 3000);

    //初始化课程数据
    this.publicPorjectData = [];//公共课程
    this.useFetchPorjectData = [];//付费课程
    this.getPublicPorjectDatas();
    this.getUserCouresPorjectDatas();

  }

  // 新方法：处理从NotebookIntegration发送的消息
  public async sendMessageToChatbot(userMessage: string): Promise<string> {
    //取消默认显示内容
    this.hideDefaultChatLog();
    // 使用现有的 handleUserInput 逻辑发送消息
    const botReply = await this.handleUserInput(userMessage);

    // 确保返回机器人的回复
    return botReply;
  }
  
  // MateGen输入API-KEY
  private bindHeaderLogoClickEvent(): void {
    return
    const headerLogoTextBox = this.node.querySelector('.header-logo-text-box') as HTMLDivElement;
    headerLogoTextBox.addEventListener('click', () => {
      this.showApiKeyModal();
    });
  }  

  private initializeDOM(): void {
    this.node.innerHTML = `
      <div class="login-container"></div>
      <div class="chatbot-container chatbox-container-rel com-scroll" style="display: none;">
      <div class="chatbot-container-box">
        <div class="sidebar">
          <div class="chatbot-container-button">
            <button id="toggle-sidebar-left" class="header-button toggle-sidebar-open"></button>
            <button id="new-chat-left" class="header-button new-welcome-base-button">️</button>
          </div>
          <div id="session-list"></div>
          <!-- 二维码和提示文字 -->
          <div class="qr-code-container">
              <div class="qr-code-in"></div>
              <div class="qr-code-text">
                <p>任何问题，扫码回复</p>
                <p>”MG“详询</p>
              </div>
          </div>
        </div>
        </div>
        <div class="chat-area">
          <div class="chat-header chat-header-btn">
            <button id="toggle-sidebar-top" class="header-button toggle-sidebar"></button>
            <button id="new-chat" class="header-button new-welcome-base-button"></button>
            <div class="header-logo-text">
              <div class="header-logo-text-box"><span><span class="header-logo">MateGen </span><span class="header-logo">Air</span></span></div>
              <div class="header-logo-title" >
                <div class="header-logo-title-span" id="toggle-title">未指定知识库</div>
                <div class="header-button header-button-user">
                  <div class="header-button-user-block">
                    <ul>
                      <li><div class="header-button chat-icon-edit"></div><p>输入API-Key(未启用)</p></li>
                      <li id="logout"><div class="header-button chat-icon-logout"></div><p>退出登录</p></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div  style="position:relative;flex:1;overflow: hidden;">
            <div id="chat-log"></div>
            <div id="chat-log-default-content" class="chatbot-body">
                
                <div class="chatbot-body-content">
                  <div class="chatbot-content-item" id="chatbot-default-edit">
                    <div class="chatbot-content-item-title">高性能自动编程<button class="header-button new-star-left new-chatbot-edit"></button></div>
                    <p>自然语言Python编程</br>一键优化代码</br>自动代码注释</br>开启变成新模式</p>
                  </div>
                  <div class="chatbot-content-item" id="chatbot-default-response">
                    <div class="chatbot-content-item-title">课程知识库问答<button class="header-button new-star-left new-chatbot-resp"></button></div>
                    <p>任何问题，随问随答</br>接入赋范空间技术社区</br>海量技术课程随时学</br>进入AI智能自习室</p>
                  </div>
                </div>
            </div>
          </div>
          <div class="chat-input">
            <div class="input-wrapper">
              <textarea class="form-control" placeholder="给MateGen发送消息..."></textarea>
              <button id="send-message" class="send-button" aria-label="Send Message"></button>
            </div>
          </div>
        </div>

        <!-- 弹出菜单容器 -->
        <div id="popup-container" class="popup-container hidden">
          <div class="popup-content">
            <div class="popup-header">
              <span>选择知识库：</span>
              <button id="close-popup" class="close-button">×</button>
            </div>
            <div class="popup-body">
              <div class="popup-head-radio-group">
                <div class="popup-head-radio-item"><input class="popup-head-radio-input" type="radio" name="porjectTypeName" value="1" id="typeName1"/><label for="typeName1">公开课知识库</label></div>
                <div class="popup-head-radio-item"><input class="popup-head-radio-input" type="radio" name="porjectTypeName" value="2" id="typeName2" /><label for="typeName2">付费课程知识库</label></div>
                <div class="popup-head-radio-item"><input class="popup-head-radio-input" type="radio" name="porjectTypeName" value="3" id="typeName3" /><label for="typeName3">自定义知识库</label></div>
              </div>
              <div class="popup-head-select-group chat-hide">
                <div class="popup-select-box">
                  <input id="selectsValue" class="popup-select-input" type="input" placeholder="请选择" data-value="" readonly/>
                  <div class="popup-select-body">
                    <ul id="select-li">
                    </ul>
                  </div>
                </div>
              </div>
              <div class="popup-select-file chat-hide">
                <input type="file" id="folderInput" webkitdirectory style="display:none;"/>
                <div class="popup-select-file-box">
                    <div class="popup-select-file-name">当前知识库名称：</div>
                    <div class="popup-select-file-content">
                        <div class="popup-select-file-btn com-btn">选择文件夹</div>
                        <div class="popup-select-file-label">该功能即将开放，敬请期待！</div>
                    </div>
                </div>
              </div>
              <div id="knowledge-status" class="chat-hide"></div>
            </div>
            <div class="popup-footer-box">
              <div class="popup-footer">
                <div class="popup-footer-desc"></div>
                <div class="popup-footer-btns">
                  <button id="reset-popup" class="popup-button">重置</button>
                  <button id="cancel-popup" class="popup-button">取消</button>
                  <button id="confirm-popup" class="popup-button confirm">确认</button>
                </div>
              </div>
            </div>
          </div>
        </div>      
      <!-- 会话条目和弹出菜单 -->
      <!-- <div id="session-item-template" class="hidden">
        <div class="session-item">
          <span class="session-name"></span>
          <div class="more-options">
            <button class="more-btn">⋮</button>
            <div class="dropdown-menu" style="display: none;">
              <button class="rename-btn">重命名</button>
              <button class="delete-btn">删除</button>
            </div>
          </div>
        </div>
        -->
      </div>
    </div>
  `;

    this.loginContainer = this.node.querySelector('.login-container') as HTMLDivElement;
    this.chatContainer = this.node.querySelector('.chatbot-container') as HTMLDivElement;
    this.chatLog = this.node.querySelector('#chat-log') as HTMLDivElement;
    this.input = this.node.querySelector('.chat-input textarea') as HTMLTextAreaElement;
    this.button = this.node.querySelector('#send-message') as HTMLButtonElement;
    this.toggleSidebarTopButton = this.node.querySelector('#toggle-sidebar-top') as HTMLButtonElement;
    this.toggleSidebarLeftButton = this.node.querySelector('#toggle-sidebar-left') as HTMLButtonElement;
    this.newChatButton = this.node.querySelector('#new-chat') as HTMLButtonElement;
    this.newChatLeftButton = this.node.querySelector('#new-chat-left') as HTMLButtonElement;
    this.sessionList = this.node.querySelector('#session-list') as HTMLDivElement;
    this.sidebar = this.node.querySelector('.sidebar') as HTMLDivElement;
    this.toggleTitle = this.node.querySelector('#toggle-title') as HTMLDivElement;
    this.toggleSidebarBg = this.node.querySelector('.chatbot-container-box') as HTMLDivElement;
    this.chatbotDefaultEdit = this.node.querySelector('#chatbot-default-edit') as HTMLDivElement;
    this.chatbotDefaultResponse = this.node.querySelector('#chatbot-default-response') as HTMLDivElement;
    this.chatLogDefaultContent = this.node.querySelector('#chat-log-default-content') as HTMLDivElement;
    this.logout = this.node.querySelector('#logout') as HTMLLIElement;
    this.btnReset = this.node.querySelector('#reset-popup') as HTMLButtonElement;
    this.selectValue = this.node.querySelector("#selectsValue") as HTMLSelectElement;
    this.typeNameClick = this.node.querySelector('.popup-head-radio-group') as HTMLDivElement;
    this.popupFooterDesc = this.node.querySelector('.popup-footer-desc') as HTMLDivElement;
    this.knowledgeStatusElement = this.node.querySelector('#knowledge-status') as HTMLDivElement;
    this.popupHeadSelectGroup = this.node.querySelector('.popup-head-select-group') as HTMLDivElement;
    this.selectBody = this.node.querySelector('.popup-select-body') as HTMLDivElement;
    this.popupSelectBox = this.node.querySelector('.popup-select-box') as HTMLDivElement;

    // MateGen相关
  this.apiKeyModal = document.createElement('div');
  this.apiKeyModal.className = 'api-key-modal hidden'; // 初始化时隐藏
  this.apiKeyModal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <span>请输入MateGen API KEY</span>
        <span class="modal-close com-btn">&times;</span>
      </div>
      <div class="modal-body">
        <div class="modal-body-content">
          <input type="text" id="api-key-input" class="api-key-input" placeholder="请输入API KEY">
          <button id="verify-api-key" class="verify-button com-btn">验证</button>
        </div>
        <div class="api-key-status hidden">API KEY验证中...</div>
      </div>
      <div class="modal-footer">
        <button id="reset-api-key" class="reset-button com-btn">重置</button>
        <button id="cancel-api-key" class="cancel-button com-btn">取消</button>
        <button id="confirm-api-key" class="confirm-button com-btn" disabled>确认</button>
      </div>
    </div>
  `;
  document.body.appendChild(this.apiKeyModal); // 将弹窗元素添加到DOM中

    this.apiKeyInput = this.apiKeyModal.querySelector('#api-key-input') as HTMLInputElement;
    this.apiKeyVerifyButton = this.apiKeyModal.querySelector('#verify-api-key') as HTMLButtonElement;
    this.apiKeyConfirmButton = this.apiKeyModal.querySelector('#confirm-api-key') as HTMLButtonElement;
    this.apiKeyCancelButton = this.apiKeyModal.querySelector('#cancel-api-key') as HTMLButtonElement;
    this.apiKeyResetButton = this.apiKeyModal.querySelector('#reset-api-key') as HTMLButtonElement;

    // 关闭弹窗
    const modalClose = this.apiKeyModal.querySelector('.modal-close') as HTMLSpanElement;
    modalClose.addEventListener('click', () => this.hideApiKeyModal());
    this.apiKeyCancelButton.addEventListener('click', () => this.hideApiKeyModal());

    // 重置按钮逻辑
    this.apiKeyResetButton.addEventListener('click', () => this.resetApiKeyInput());

    // 验证按钮逻辑
    this.apiKeyVerifyButton.addEventListener('click', () => this.verifyApiKey());

    // 禁用确认按钮，除非API验证通过
    this.apiKeyConfirmButton.addEventListener('click', () => this.confirmApiKey());

    // 绑定 header-logo-text-box 的点击事件
    this.bindHeaderLogoClickEvent();  // 在初始化时调用此函数
    // 设置默认显示状态
    this.updateLogoTextAndStyle(); // 调用该函数来设置初始状态
  }
  
  // MateGen相关
  private async verifyApiKey(): Promise<void> {
	  const apiKey = this.apiKeyInput.value.trim();
	  this.encryptedApiKey = apiKey;
	  const statusElement = this.apiKeyModal.querySelector('.api-key-status') as HTMLDivElement;
	
	  if (apiKey) {
	    statusElement.textContent = 'API KEY解析中...';
	    statusElement.classList.remove('hidden');
	
	    // 调用后端API进行解密
	    try {
	      const response = await fetch('http://mate.wsp2.cn/verify-api-key', {
	        method: 'POST',
	        headers: {
	          'Content-Type': 'application/json',
	        },
	        body: JSON.stringify({ encrypted_api_key: apiKey }),
	      });
	
	      const data = await response.json();
	      if (data.status === 'success') {
	        const decryptedApiKey = data.decrypted_api_key;
	        statusElement.textContent = '正在验证API-KEY...';
	
	        // 使用解密后的API Key进行OpenAI服务验证
	        const isValid = await this.verifyWithOpenAI(decryptedApiKey);
	
	        if (isValid) {
	          statusElement.textContent = 'API-KEY验证通过！';	          
	          
	          // 在API-KEY验证通过后，进行Assistant的创建和日志记录
	          this.decryptedApiKey = decryptedApiKey; // 先将解密后的API Key暂存

	          // 自动调用 Assistant 创建和日志记录逻辑
	          await this.onApiKeyVerified(decryptedApiKey);
               // 启用确认按钮
	          this.apiKeyConfirmButton.disabled = false; // 启用确认按钮
	          
	        } else {
	          statusElement.textContent = 'API-KEY无效，无法连接到MateGen服务。';
	          this.apiKeyConfirmButton.disabled = true; // 禁用确认按钮
	        }
	      } else {
	        statusElement.textContent = data.message;
	        this.apiKeyConfirmButton.disabled = true; // 禁用确认按钮
	      }
	    } catch (error) {
	      statusElement.textContent = '验证过程中出现错误，请重试！';
	      this.apiKeyConfirmButton.disabled = true;
	    }
	  } else {
	    statusElement.textContent = '请输入有效的API KEY';
	  }
	}
	
	private async verifyWithOpenAI(apiKey: string): Promise<boolean> {
	  try {
	    const response = await fetch('https://api.openai.com/v1/engines', {
	      method: 'GET',
	      headers: {
	        'Authorization': `Bearer ${apiKey}`,
	      },
	    });
	
	    if (response.ok) {
	      return true; // 验证成功
	    } else {
	      console.error('MateGen验证失败', await response.text());
	      return false; // 验证失败
	    }
	  } catch (error) {
	    console.error('无法连接到MateGen服务', error);
	    return false; // 验证失败
	  }
	}
  private async onApiKeyVerified(apiKey: string): Promise<void> {
    await this.manageAssistant();
  }

  private showApiKeyModal(): void {
    this.apiKeyModal.classList.remove('hidden');
    this.apiKeyModal.style.display = 'flex';
  }

  private hideApiKeyModal(): void {
    this.apiKeyModal.classList.add('hidden');
    this.apiKeyModal.style.display = 'none';
  }

private resetApiKeyInput(): void {
  // 清空输入框的值
  this.apiKeyInput.value = '';

  // 将确认按钮设置为禁用状态
  this.apiKeyConfirmButton.disabled = true;

  // 清除解密后的 API Key
  this.decryptedApiKey = null;

  // 清除存储的 MateGen API Key，表示切换回 GLM 模型
  this.mateGenApiKey = '';

  // 重置 API 服务，以便切换回 GLM 模型
  this.apiService = new ApiService(this.mateGenApiKey);

  // 更新 UI 状态以显示默认的 MateGen Air 字样
  this.updateLogoTextAndStyle();

  // 隐藏验证状态信息
  const statusElement = this.apiKeyModal.querySelector('.api-key-status') as HTMLDivElement;
  statusElement.classList.add('hidden');
  statusElement.textContent = '';

  // 关闭弹窗
  this.hideApiKeyModal();
  
  //初始化课程数据
  this.getPublicPorjectDatas();
  this.getUserCouresPorjectDatas();

  console.log('API Key 已重置，切换为 GLM 模型');
}


private async confirmApiKey(): Promise<void> {
  if (this.decryptedApiKey) {
    this.mateGenApiKey = this.decryptedApiKey; // 将解密后的API Key赋值给mateGenApiKey
    this.apiService = new ApiService(this.mateGenApiKey); 
    //初始化课程数据
    this.getPublicPorjectDatas();
    this.getUserCouresPorjectDatas();
    console.log('API Key已确认并设置:', this.mateGenApiKey);
    
    // 更新 header-logo-text-box 的显示内容和样式
    this.updateLogoTextAndStyle();
    
    this.hideApiKeyModal(); // 隐藏弹窗
  } else {
    console.error('API Key无效，无法使用');
  }
}
// 初始化时或重置时调用，显示默认状态
private updateLogoTextAndStyle(): void {
  const headerLogoTextBox = this.node.querySelector('.header-logo-text-box') as HTMLDivElement;
  
  if (this.mateGenApiKey && this.mateGenApiKey !== '') {
    // 如果API Key已设置，显示 "MateGen Pro"，并应用黄色字体
    headerLogoTextBox.innerHTML = '<span><span class="header-logo">MateGen </span><span class="header-logo">Pro</span></span>';
    headerLogoTextBox.classList.remove('header-logo-air');
    headerLogoTextBox.classList.add('header-logo-pro');
  } else {
    // 如果API Key为空，显示 "MateGen Air"，并应用白色字体
    headerLogoTextBox.innerHTML = '<span><span class="header-logo">MateGen </span><span class="header-logo">Air</span></span>';
    headerLogoTextBox.classList.remove('header-logo-pro');
    headerLogoTextBox.classList.add('header-logo-air');
  }
}
  // 1. 检查或创建.log日志文件
  private async checkOrCreateLogFile(): Promise<void> {
    try {
      await this.contents.get(this.LOG_FILE);
    } catch (error) {
      await this.contents.save(this.LOG_FILE, {
        type: 'file',
        format: 'text',
        content: ''
      });
    }
  }
  
  // 检查或创建知识库日志文件和文件夹
  private async checkOrCreateKnowledgeBaseFileAndFolder(): Promise<void> {
    try {
      // 检查或创建知识库日志文件
      await this.contents.get(this.KNOWLEDGE_BASE_FILE);
    } catch (error) {
      await this.contents.save(this.KNOWLEDGE_BASE_FILE, {
        type: 'file',
        format: 'text',
        content: ''
      });
    }

    try {
      // 检查或创建知识库文件夹
      await this.contents.get(this.KNOWLEDGE_BASE_FOLDER);
    } catch (error) {
      await this.contents.save(this.KNOWLEDGE_BASE_FOLDER, {
        type: 'directory',
        format: null,  // 对于目录，format 应为 null 或省略
        content: ''
      });
    }
  }



  
  // 2. 读取日志文件内容
  private async readLogFile(): Promise<any[]> {
    try {
      const logFile = await this.contents.get(this.LOG_FILE, { format: 'text', content: true });
      const logEntries = logFile.content
        .split('\n')
        .filter((line: string) => line)
        .map((line: string) => JSON.parse(line));
      return logEntries;
    } catch (error) {
      console.error('Error reading log file:', error);
      return [];
    }
  }
  // 3. 将新的API-KEY和assistant_id写入.log文件
  private async writeToLogFile(apiKey: string, assistantId: string): Promise<void> {
    const newEntry = { apiKey: this.encryptedApiKey, assistantId };

    try {
      const logEntries = await this.readLogFile();
      logEntries.push(newEntry);

      const logContent = logEntries.map(entry => JSON.stringify(entry)).join('\n');
      await this.contents.save(this.LOG_FILE, {
        type: 'file',
        format: 'text',
        content: logContent
      });
    } catch (error) {
      console.error('Error writing to log file:', error);
    }
  }
  // 4. 查找日志文件中是否存在当前API-KEY的assistant_id
  private async findAssistantInLog(): Promise<string | null> {
    const logEntries = await this.readLogFile();
    const entry = logEntries.find(log => log.apiKey === this.encryptedApiKey);
    return entry ? entry.assistantId : null;
  }

  // 5. 创建Assistant逻辑
private async createAssistant(): Promise<string> {
  try {
    // 检查 decryptedApiKey 是否为 null
    if (!this.decryptedApiKey) {
      throw new Error('API-KEY 未定义');
    }

    // 使用解密后的 API-KEY 创建 OpenAI 实例
    const openai = new OpenAI({ 
    	apiKey: this.decryptedApiKey as string,
    	dangerouslyAllowBrowser: true
    	});

    const assistant = await openai.beta.assistants.create({
      instructions: '你是九天老师团队开发的MateGen，一款多功能聊天对话机器人',
      name: 'MateGen',
      model: 'gpt-4o',
    });

    console.log('Assistant 创建成功:', assistant.id);
    return assistant.id;
  } catch (error) {
    console.error('创建 Assistant 时出错:', error);
    throw new Error('Assistant 创建失败');
  }
}
  
  // 6. 管理Assistant的核心逻辑
  private async manageAssistant(): Promise<void> {
    let assistantId = await this.findAssistantInLog();

    if (assistantId) {
      // 检查 assistant_id 是否有效
      const exists = await this.checkAssistantExists(assistantId);

      if (!exists) {
        // 如果当前 assistant_id 不存在，重新创建一个
        assistantId = await this.createAssistant();
        await this.writeToLogFile(this.encryptedApiKey!, assistantId);
      }
    } else {
      // 如果日志中没有该 API-KEY，则创建新 assistant
      assistantId = await this.createAssistant();
      await this.writeToLogFile(this.encryptedApiKey!, assistantId);
    }

    this.assistantId = assistantId; // 保存 assistant_id
    console.log('当前使用的 assistant_id:', assistantId);
  }

private async checkAssistantExists(assistantId: string): Promise<boolean> {
  try {
    // 检查 decryptedApiKey 是否为 null
    if (!this.decryptedApiKey) {
      throw new Error('API-KEY 未定义');
    }

    // 使用解密后的 API-KEY 检查 Assistant
    const openai = new OpenAI({ 
    	apiKey: this.decryptedApiKey as string,
    	dangerouslyAllowBrowser: true
    	});

    const myAssistant = await openai.beta.assistants.retrieve(assistantId);
    console.log('Assistant 存在:', myAssistant.id);
    return true; // assistant_id 存在
  } catch (error) {
    console.error('Assistant 不存在或检索出错:', error);
    return false; // assistant_id 不存在
  }
} 

  private bindEventHandlers(): void {
    const _this = this;
    this.button.addEventListener('click', async () => {
      this.hideDefaultChatLog();
      await this.handleUserInput(); // 等待 handleUserInput 完成，但不需要处理返回值
    });

    this.input.addEventListener('keypress', async (event: KeyboardEvent) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.hideDefaultChatLog();
        await this.handleUserInput(); // 同样等待执行完成
      }
    });
    this.input.addEventListener('input', () => autoResizeTextarea(this.input));
    this.toggleSidebarTopButton.addEventListener('click', () =>
      this.toggleSidebar()
    );
    this.toggleSidebarLeftButton.addEventListener('click', (event: Event) => {
      event.stopPropagation();
      this.toggleSidebar();
    });
    this.toggleSidebarBg.addEventListener('click', function (event: Event) {
      event.stopPropagation();
      _this.toggleSidebar();
    });
    this.newChatButton.addEventListener('click', () => {
      this.createNewSession();
      this.initDefaultChatLog(); // 初始化默认会话内容
    });
    this.newChatLeftButton.addEventListener('click', (event: Event) => {
      event.stopPropagation();
      this.toggleSidebar();
      this.createNewSession();
      this.initDefaultChatLog(); // 初始化默认会话内容
    });

    //自动编程
    this.chatbotDefaultEdit.addEventListener('click', () => {
      this.createNewSession();//初始化会话内容
      this.hideDefaultChatLog();//取消默认显示内容
      this.input.value = "如何借助MateGen进行高性能全自动编程呢？";
      this.handleUserInput('', 'edit');
    });

    //自动问答
    this.chatbotDefaultResponse.addEventListener('click', () => {
      this.createNewSession();//初始化会话内容
      this.hideDefaultChatLog();//取消默认显示内容
      this.input.value = "如何借助MateGen开启课程知识库问答呢？";
      this.handleUserInput('', 'resp');//发送会话消息
    });

    // 
    this.toggleTitle.addEventListener('click', () => {
      const toggleTitleTextContent = this.toggleTitle.textContent;
      toggleTitleTextContent ? this.queryOpenPopup() : null;
    });

    //退出登录
    this.logout.addEventListener('click', e => {
      e.stopPropagation();
      this.publicPorjectData = [];//公共课程
      this.useFetchPorjectData = [];//付费课程
      this.goToLoginManagerPage();//显示登录页面
    });

	// 重置知识库
	this.btnReset.addEventListener('click', () => {
	  this.selectValue.value = ""; // 清空知识库选择的值
	  this.knowledgeStatusElement.classList.add('chat-hide'); // 隐藏知识库状态元素
	  this.popupFooterDesc.textContent = ""; // 清空弹窗底部描述
	  this.toggleTitle.textContent = '未选定学习课程'; // 更新标题为未选定课程
	  this.apiService = new ApiService(); // 创建新的 API 服务实例
	  this.selectBody.classList.remove('popup-select-show'); // 隐藏选择列表
    this.popupSelectBox.classList.remove('popup-select-box-show');
	});

    //选择课程类型-切换数据源
    this.typeNameClick.addEventListener('click', (e) => {
      e.stopPropagation();

      //取消下拉
      this.selectBody.classList.remove('popup-select-show');
      this.popupSelectBox.classList.remove('popup-select-box-show');

      //初始化错误信息状态
      this.knowledgeStatusElement.textContent = "";

      //初始化课程选中值
      this.selectValue.value = "";

      //获取课程类型信息
      this.knowledgeStatusElement.classList.add('chat-hide');
      setTimeout(() => {
        const porjectTypeValue = this.node.querySelector("input[name='porjectTypeName']:checked") as HTMLInputElement;
        const selectValueBox = this.node.querySelector('#select-li') as HTMLUListElement;
        const popupSelectFile = this.node.querySelector(".popup-select-file") as HTMLButtonElement;
        const customFile = this.node.querySelector(".popup-select-file-btn") as HTMLButtonElement;
        let tempOtion = "";
        //自定义知识库
        if(porjectTypeValue.value === "3"){
          this.popupHeadSelectGroup.classList.add('chat-hide');
          popupSelectFile.classList.remove('chat-hide');
          return
          customFile.addEventListener('click',(e)=>{
            e.stopPropagation();
            console.log("1111111111111111111111111")
            this.customFileContent()
          })
          return
        }
        //公开课程
        popupSelectFile.classList.add('chat-hide');
        this.popupHeadSelectGroup.classList.remove('chat-hide');
        if (porjectTypeValue.value === "1") {
          tempOtion = this.initPorjectData(this.publicPorjectData);
        }
        //付费课程
        if (porjectTypeValue.value === "2") {
          tempOtion = this.initPorjectData(this.useFetchPorjectData);
          //没有付费课程提示
          if (this.useFetchPorjectData.length === 0) {
            //取消选择课程显示
            this.popupHeadSelectGroup.classList.add('chat-hide');
            this.knowledgeStatusElement.classList.remove('chat-hide');
            this.knowledgeStatusElement.innerHTML = `<div style="width:205px;">您还未注册课程平台，戳此完成注册：</div><a href="https://appze9inzwc2314.h5.xiaoeknow.com" target="_blank" style="text-dec">点击注册</a>`;
          }
        }
        selectValueBox.innerHTML = tempOtion;
        this.selectValue.value = "";
        setTimeout(()=>{
          //课程选择
          const liAll = this.node.querySelectorAll(".popup-select-li")
          liAll.forEach((k,index)=>{
            k.addEventListener('click',(e)=>{
              //课程类型
              const type = this.node.querySelector("input[name='porjectTypeName']:checked") as HTMLInputElement;
              let selectDatas = type.value==="1"?this.publicPorjectData:type.value==="2"?this.useFetchPorjectData:[];
              const currentSelectData =selectDatas.filter((k,i)=>i===index);
              const curObj:PorjectItemInterface = currentSelectData.length>0?currentSelectData[0]:{id:"",name:""};
              this.selectValue.value=curObj.name;
              this.selectBody.classList.remove('popup-select-show');
              this.popupSelectBox.classList.remove('popup-select-box-show');
            })
          })
        },100)
      }, 100)
    })

    //视口大小变化监听
    this.listenerDivResize();

    //显示关闭select
    this.selectValue.addEventListener('click',()=>{
      const hasIndex = this.selectBody.className.indexOf('popup-select-show');
      if(hasIndex===-1){
        this.selectBody.classList.add('popup-select-show');
        this.popupSelectBox.classList.add('popup-select-box-show');
      }else{
        this.selectBody.classList.remove('popup-select-show');
        this.popupSelectBox.classList.remove('popup-select-box-show');
      }
    })

    this.bindPopupEventHandlers();
  } 

  //监听视口大小变化
  private listenerDivResize(){
    const _this=this;
    const chatAarea = this.node.querySelector('.chat-area') as HTMLDivElement
    const observer = new ResizeObserver((entries) => {
      let wid = 0;
      _this.debounce((()=>{
        const headerLogoTextBox = _this.node.querySelector('.header-logo-text-box') as HTMLDivElement;
        const chatLogDefaultContent = _this.node.querySelector('#chat-log-default-content') as HTMLDivElement;
        const chatbotBodyContent = _this.node.querySelector('.chatbot-body-content') as HTMLDivElement;
        wid = _this.getElementWidth('.chatbot-container');
        if(wid<=360){
          headerLogoTextBox.style.display="none";
        }else{
          headerLogoTextBox.style.display="block";
        }
        if(wid<=430){
          chatLogDefaultContent.style.width="213px";
          chatLogDefaultContent.style.marginLeft="-106px";
          chatLogDefaultContent.style.marginTop="-205px";
          chatbotBodyContent.style.display="block";
        }else{
          chatLogDefaultContent.style.width="430px";
          chatLogDefaultContent.style.marginLeft="-215px";
          chatLogDefaultContent.style.marginTop="-86px";
          chatbotBodyContent.style.display="flex";
        }
      })(),2000)
    });
    observer.observe(chatAarea);
  }

  private customFileContent():void{
    //自定义知识库
    const folderInput = this.node.querySelector("#folderInput") as HTMLInputElement;
    return
    folderInput.click();
    folderInput.addEventListener('change',async (event)=>{
      // const files = (event.target as HTMLInputElement).files;
      // if (!files||!files.length) {
      //     console.log('No folder selected');
      //     return;
      // }
      // const filePath = files[0].webkitRelativePath; // 获取文件夹路径
      // const fileNN = URL.createObjectURL(files[0]);
      // console.log('Selected folder path:', files,filePath,fileNN);

      const vectorstoreId = 'vs_8TYIE9ujhXPodHBDr58HONvm'
      const openai = new OpenAI({ 
        apiKey: this.decryptedApiKey as string,
        dangerouslyAllowBrowser: true
      });

      this.uploadDocumentsFromFolder(openai,folderInput,vectorstoreId)

    })
  };

  private async uploadDocumentsFromFolder(openai: OpenAI, folderInput: HTMLInputElement, vectorStoreId: string): Promise<void> {
    // 获取用户选择的文件列表
    const files = folderInput.files;
  
    if (!files || files.length === 0) {
      console.warn('没有选择任何文件');
      return;
    }
  
    for (let file of files) {
      try {
        // 使用 File API 读取文件内容
        const fileContent = await file.text();
  
        // 使用 fetch 上传文件到 OpenAI 的文件系统
        const response = await fetch('https://api.openai.com/v1/files', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.mateGenApiKey}`,
            'Content-Type': 'multipart/form-data'
          },
          body: new Blob([fileContent], { type: file.type || 'text/plain' }) // 使用 Blob 来处理文件内容
        });
  
        if (!response.ok) {
          console.warn(`文件上传失败，跳过: ${file.name}`);
          continue;
        }
  
        const data = await response.json();
        const fileId = data.id;
  
        // 将文件添加到知识库
        await openai.beta.vectorStores.files.create(vectorStoreId, {
          file_id: fileId
        });
  
        console.log(`文件 ${file.name} 上传并添加到知识库成功`);
      } catch (error) {
        console.warn(`文件处理失败，跳过: ${file.name}`);
      }
    }
  }

  //获取元素宽度
  private getElementWidth(className:string):number{
    const currentDiv = this.node.querySelector(className) as HTMLDivElement;
    const style  = window.getComputedStyle(currentDiv) 
    const wid = currentDiv.clientWidth + parseFloat(style.marginLeft) + parseFloat(style.marginRight);
    return wid;
  }

  //选择课程初始化课程信息
  private initPorjectData(arr: Array<PorjectItemInterface>): string {
    const tempOptions = arr.map(k => `<li class="popup-select-li">${k.name}</li>`);
    return tempOptions.join("");
  }

  //初始化当前页面信息
  private initCurrentChatbotWidgetPage(): void {
    localStorage.clear();//清除登录信息
    this.createNewSession();
    this.initDefaultChatLog();//初始化会话内容
    this.initDefaultchatContainer();//初始化当前页
  }

  //跳转登录页
  private goToLoginManagerPage(): void {
    this.loginManager = new LoginManager(
      this.loginContainer,
      this.onLoginSuccess.bind(this)
    );
    this.initCurrentChatbotWidgetPage();//初始化当前页面信息
    this.loginManager.showLoginInterface();//显示登录页
  }

  //知识库弹框确定
  private async queryOpenPopup(): Promise<void> {
    const popupContainer = this.node.querySelector('#popup-container') as HTMLDivElement;
    if (this.popupFooterDesc) {
      // this.popupFooterDesc.textContent = '知识库正在查询中...';
    }
    const courseNumber = await this.apiService.getCourseNumberByKnowledgeId();
    if (this.popupFooterDesc) {
      if (courseNumber === '未设置知识库' || courseNumber === '') {
        // this.popupFooterDesc.textContent = '';
      } else {
        // this.popupFooterDesc.textContent = `当前知识库：${this.formatStringFn(courseNumber)}`;
      }
    }
    popupContainer.classList.remove('hidden');
  }

  private bindPopupEventHandlers(): void {
    const closePopupButton = this.node.querySelector('#close-popup') as HTMLButtonElement;
    const cancelPopupButton = this.node.querySelector('#cancel-popup') as HTMLButtonElement;
    const confirmPopupButton = this.node.querySelector('#confirm-popup') as HTMLButtonElement;
    const popupContainer = this.node.querySelector('#popup-container') as HTMLDivElement;

    closePopupButton.addEventListener('click', () => {
      popupContainer.classList.add('hidden');
      this.selectBody.classList.remove('popup-select-show');
      this.popupSelectBox.classList.remove('popup-select-box-show');
    });

    cancelPopupButton.addEventListener('click', () => {
      popupContainer.classList.add('hidden');
      this.selectBody.classList.remove('popup-select-show');
      this.popupSelectBox.classList.remove('popup-select-box-show');
    });

    confirmPopupButton.addEventListener('click', async () => {
      const porjectTypeValue = this.node.querySelector("input[name='porjectTypeName']:checked") as HTMLInputElement;
      const courseNumber = this.formatStringFn(this.selectValue.value,formatStringInterface.name,formatStringInterface.id);
      if (!courseNumber && !porjectTypeValue) {
        this.knowledgeStatusElement.textContent = "请先选择课程知识库";
        return;
      }

      let courseNumberNew = courseNumber; // 提取到外部作用域，确保在所有分支中都可以访问
      
      this.toggleTitle.textContent = '未选定学习课程';
      this.selectBody.classList.remove('popup-select-show');
      this.popupSelectBox.classList.remove('popup-select-box-show');
      
      try {
      	if (this.mateGenApiKey) {
	      // 如果有 MateGen API Key，则重新获取courseNumber
		const openai = new OpenAI({
		      apiKey: this.mateGenApiKey,
		      dangerouslyAllowBrowser: true
		    });
		    
		if (courseNumber.startsWith('http')) {
		      courseNumberNew = await this.handleKnowledgeIdUrl(openai, courseNumber);
		    } else {
		      courseNumberNew = await this.handleLocalKnowledgeFolder(openai, courseNumber);
		    }
	    }
	    
          this.apiService.setKnowledgeId(courseNumberNew);
          
          this.toggleTitle.textContent = `正在学习：${this.formatStringFn(courseNumberNew)}`;
          this.knowledgeStatusElement.style.display = "none";
          localStorage.setItem("courseNumber", courseNumberNew);
          popupContainer.classList.add('hidden');//取消弹出显示
          
      } catch (error) {
        if (this.knowledgeStatusElement) {
          this.knowledgeStatusElement.classList.remove('chat-hide');
          this.knowledgeStatusElement.textContent = '网络错误，请稍后重试';
        }
      }
    });
  }

  private initializeLoginManager(): void {
    this.loginManager = new LoginManager(
      this.loginContainer,
      this.onLoginSuccess.bind(this)
    );
    const isLoggedIn = this.loginManager.checkLoginStatusOnLoad();
    if (isLoggedIn) {
      this.showChatInterface();
    } else {
      this.loginManager.showLoginInterface();
    }
  }

  private onLoginSuccess(token: string): void {
    console.log('Login successful, JWT:', token);
    this.showChatInterface();
  }

  private showChatInterface(): void {
    if (this.loginManager) {
      this.loginManager.hideLoginInterface();
    }
    this.chatContainer.style.display = 'flex';
    this.sidebar.classList.add('sidebar-hidden');
    this.loadSessions();

    //初始化课程数据
    this.getPublicPorjectDatas();
    this.getUserCouresPorjectDatas();
  }

  private configureMarked(): void {
    marked.use(
      markedHighlight({
        langPrefix: 'language-',
        highlight(code, lang) {
          if (lang && Prism.languages[lang]) {
            return Prism.highlight(code, Prism.languages[lang], lang);
          }
          return code;
        }
      })
    );
  }

  // 定义创建 Assistant 线程 ID 的函数
  private async createAssistantThread(): Promise<string> {
    try {
      // 创建 OpenAI 客户端，使用解密后的 API Key
      const openai = new OpenAI({ 
	    	apiKey: this.decryptedApiKey as string,
	    	dangerouslyAllowBrowser: true
	    	});

      // 调用 Assistant API 创建新的线程
      const emptyThread = await openai.beta.threads.create();

      console.log('线程创建成功:', emptyThread.id);
      return emptyThread.id; // 返回新创建的线程 ID
    } catch (error) {
      console.error('创建 Assistant 线程时出错:', error);
      throw new Error('Assistant 线程创建失败');
    }
  }

  // 定义检查线程 ID 是否存在的函数
	private async checkThreadExists(threadId: string): Promise<boolean> {
	  try {
	    // 创建 OpenAI 客户端，使用解密后的 API Key
	    const openai = new OpenAI({ 
	      apiKey: this.decryptedApiKey as string,
	      dangerouslyAllowBrowser: true
	    });
	
	    // 调用 Assistant API 获取线程信息
	    const myThread = await openai.beta.threads.retrieve(threadId);
	    console.log('线程存在:', myThread.id);
	    return true; // 线程 ID 有效
	  } catch (error) {
	    console.error('线程不存在或检索出错:', error);
	    return false; // 线程 ID 无效
	  }
	}

private async getLatestAssistantMessage(threadId: string, userMessageSentTime: number): Promise<string> {
  try {
    // 创建 OpenAI 客户端
    const openai = new OpenAI({
      apiKey: this.decryptedApiKey as string,
      dangerouslyAllowBrowser: true
    });

    const maxAttempts = 5; // 最多尝试 5 次
    const waitTime = 5000; // 每次等待 5 秒

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      // 获取线程中的消息列表
      const threadMessages = await openai.beta.threads.messages.list(threadId);

      // 过滤出所有的 Assistant 回复，并且确保它的时间戳是在用户消息发送之后
      const assistantMessages = threadMessages.data.filter(
        (message: any) => message.role === 'assistant' && message.created_at > userMessageSentTime
      );

      // 如果找到了有效的 Assistant 回复
      if (assistantMessages.length > 0) {
        // 获取最新的 Assistant 回复
        const latestAssistantMessage = assistantMessages[0]; // 因为消息是新到旧排序，第一个就是最新的

        if (latestAssistantMessage && latestAssistantMessage.content.length > 0) {
          const contentBlock = latestAssistantMessage.content[0];
          if (contentBlock.type === 'text' && contentBlock.text?.value) {
            return contentBlock.text.value; // 返回最新的机器人回复
          }
        }
      }

      // 如果没有找到合适的回复，则等待并重试
      console.log(`第 ${attempt + 1} 次尝试获取 Assistant 回复，未找到，等待中...`);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }

    console.warn('在尝试数次后未找到合适的 Assistant 回复消息文本内容。');
    return '';
  } catch (error) {
    console.error('获取 Assistant 线程消息时出错:', error);
    throw new Error('Assistant 线程消息获取失败');
  }
}
private async handleUserInput(userMessage?: string, typeName?: string): Promise<string> {
  // 如果传入了 userMessage，则表示消息来自 cell
  const userInput = userMessage ? userMessage : this.input.value.trim();

  if (userInput) {
    // 如果没有当前会话（即为 null），则创建新的会话
    if (!this.currentSession) {
      const firstMessage: Message = { role: 'user', content: userInput };
      this.currentSession = await this.sessionManager.createNewSessionOnFirstMessage(firstMessage); // 创建会话并保存

      // 添加用户消息到聊天记录
      await this.addMessage(userInput, 'user-message');
    } else {
      // 打印用户消息到聊天记录
      await this.addMessage(userInput, 'user-message');

      // 添加用户消息到当前会话
      this.currentSession.messages.push({ role: 'user', content: userInput });

      // 保存当前会话到文件
      await this.sessionManager.saveSessionToFile(this.currentSession);
    }

    this.loadSessions(); // 每次用户发送消息后刷新会话列表

    // 在这里清空输入框
    if (!userMessage) {
      this.input.value = '';
      this.input.style.height = '30px'; // 重置输入框高度
    }

    this.input.placeholder = '正在等待回复...';
    this.input.disabled = true;

    try {
      // 判断是否使用 Assistant API 或 GLM 模型
      if (this.mateGenApiKey && this.currentSession) {
        // 使用 Assistant API 进行对话
        let threadId = this.currentSession.mg_id;

        // 验证线程 ID 是否存在
        if (threadId) {
          const isValidThread = await this.checkThreadExists(threadId);
          if (!isValidThread) {
            // 如果线程 ID 无效，重新创建一个新的线程
            threadId = await this.createAssistantThread();
            this.currentSession.mg_id = threadId;

            // 保存会话以更新 mg_id
            await this.sessionManager.saveSessionToFile(this.currentSession);
          }
        } else {
          // 如果线程 ID 不存在，创建一个新的线程
          threadId = await this.createAssistantThread();
          this.currentSession.mg_id = threadId;

          // 保存会话以更新 mg_id
          await this.sessionManager.saveSessionToFile(this.currentSession);
        }

        // 记录用户消息的时间戳
        const userMessageSentTime = Math.floor(Date.now() / 1000);

        let accumulatedBotReply = ''; // 用于存储完整的机器人回复

        // 添加一条占位符消息，表示机器人正在回复
        let lastMessageId = await this.addMessage('', 'bot-message', true);

        // 检查 lastMessageId 是否为 string
        if (typeof lastMessageId === 'string') {
          // 使用流式回复，逐步更新最后一条消息
          await this.apiService.getBotReply(
            this.getLimitedContextMessages(),
            this.assistantId!,
            threadId,
            (messageChunk: string) => {
              accumulatedBotReply += messageChunk; // 将新接收到的消息块累加
              this.updateLastMessage(lastMessageId as string, accumulatedBotReply); // 更新最后一条消息内容
              this.chatLog.scrollTop = this.chatLog.scrollHeight; // 每次收到消息后滚动到底部
            }
          );
          //处理代码块内容
          this.formatCodeBlockHtmlFn(lastMessageId as string)
        } else {
          console.error('Failed to create message or get message ID.');
        }
        // 获取线程的最新机器人回复消息
        const latestAssistantMessage = await this.getLatestAssistantMessage(threadId, userMessageSentTime);

        // 当所有消息接收完毕后，处理会话记录等逻辑
        if (this.currentSession) {
          this.currentSession.messages.push({
            role: 'assistant',
            content: latestAssistantMessage // 保存完整的机器人回复
          });

          // 保存会话并更新显示
          await this.sessionManager.saveSessionToFile(this.currentSession);
        }
      } else {
        // 使用 GLM 模型进行对话
        let accumulatedBotReply = ''; // 用于存储完整的机器人回复

        // 添加一条占位符消息，表示机器人正在回复
        let lastMessageId = await this.addMessage('', 'bot-message', true);

        // 检查 lastMessageId 是否为 string
        if (typeof lastMessageId === 'string') {
          // 使用流式回复，逐步更新最后一条消息
          await this.apiService.getBotReply(
            this.getLimitedContextMessages(),
            (messageChunk: string) => {
              accumulatedBotReply += messageChunk; // 将新接收到的消息块累加
              this.updateLastMessage(lastMessageId as string, accumulatedBotReply); // 更新最后一条消息内容
              this.chatLog.scrollTop = this.chatLog.scrollHeight; // 每次收到消息后滚动到底部
            }
          );
          //处理代码块内容
          this.formatCodeBlockHtmlFn(lastMessageId as string)
        } else {
          console.error('Failed to create message or get message ID.');
        }

        // 当所有消息接收完毕后，处理会话记录等逻辑
        if (this.currentSession) {
          this.currentSession.messages.push({
            role: 'assistant',
            content: accumulatedBotReply // 保存完整的机器人回复
          });

          // 保存会话并更新显示
          await this.sessionManager.saveSessionToFile(this.currentSession);
        }
      }

      this.loadSessions(); // 回复后刷新会话列表并排序
      this.chatLog.scrollTop = this.chatLog.scrollHeight; // 滚动到最新的消息
    } catch (error) {
      await this.addMessage('抱歉，出现了错误。请稍后再试。', 'error-message');
      console.error('Error during bot reply:', error);
    }

    this.input.placeholder = '给MateGen发送消息...';
    this.input.disabled = false;
  }

  if (!userMessage) {
    // 如果 userMessage 为空，表示这是来自用户聊天框的输入，处理输入框和按钮的状态
    this.input.value = '';
    this.input.style.height = '30px';
    this.input.disabled = true;
    this.button.disabled = true;
  }

  // 恢复输入框和按钮状态
  if (!userMessage) {
    this.input.value = '';
    this.input.disabled = false;
    this.button.disabled = false;
    this.input.focus();
  }

  return '无回复'; // 如果没有输入则返回默认回复
}

  private async updateLastMessage(messageId: string, newContent: string): Promise<void> {
    const messageElement = document.getElementById(messageId);
  
    if (messageElement) {
      let tempBuffer = '';  // 用于暂存普通文本
      let isCodeBlock = false;
      let codeLang = '';
  
      // 新增：当前代码元素
      let currentCodeElement: HTMLElement | null = null;
  
      // 清空现有的文字内容，以避免重复
      let textContainer = messageElement.querySelector('.text-content');
      let codeContainer = messageElement.querySelector('.code-content');
  
      // 如果 textContainer 或 codeContainer 不存在，则创建它们
      if (!textContainer) {
        textContainer = document.createElement('div');
        textContainer.className = 'text-content';
        messageElement.appendChild(textContainer);
      }
  
      if (!codeContainer) {
        codeContainer = document.createElement('div');
        codeContainer.className = 'code-content';
        messageElement.appendChild(codeContainer);
      }
  
      const lines = [newContent.trim()];  // 新的一段流式内容
  
      for (const line of lines) {
        if (line.startsWith('```')) {
          if (isCodeBlock) {
            // 代码块结束
            isCodeBlock = false;
            currentCodeElement = null;  // 重置当前代码元素
          } else {
            // 代码块开始，创建一个新的代码框
            codeLang = line.slice(3).trim();  // 获取代码语言
            isCodeBlock = true;
            
            // 创建代码框并插入到 codeContainer 中
            const codeWrapper = document.createElement('div');
            codeWrapper.className = 'code-wrapper';
            codeWrapper.innerHTML = `
              <div class="code-header">
                <span class="code-language">${codeLang}</span>
                <button class="copy-button">复制</button>
              </div>
              <pre><code class="language-${codeLang}"></code></pre>
            `;
            codeContainer.appendChild(codeWrapper);
            
            // 获取当前代码块的 <code> 元素
            currentCodeElement = codeWrapper.querySelector('code');
            
            // 实现复制按钮功能
            const copyButton = codeWrapper.querySelector('.copy-button');
            if (copyButton && currentCodeElement) {
              copyButton.addEventListener('click', () => {
                copyCodeToClipboard(currentCodeElement!);
              });
            }
          }
        } else if (isCodeBlock) {
          // 处于代码块中，逐行流式打印代码
          if (currentCodeElement) {
            currentCodeElement.textContent += line + '\n';  // 追加代码行到当前代码框中
            Prism.highlightElement(currentCodeElement);  // 高亮处理
            // 强制浏览器渲染
            currentCodeElement.offsetHeight;
          }
        } else {
          // 对于普通文本，处理并流式打印
          tempBuffer += line + ' ';
          if (line.endsWith('.') || line.endsWith('。') || line.endsWith(',')) {
            const renderedContent = await marked.parse(tempBuffer);
            const sanitizedContent = DOMPurify.sanitize(renderedContent);
            if (textContainer) {
              textContainer.innerHTML = sanitizedContent;  // 更新普通文本内容
            }
            tempBuffer = '';  // 清空缓冲区
          }
        }
      }
  
      // 如果有残留的普通文本，插入最后一部分
      if (tempBuffer.trim()) {
        const renderedContent = await marked.parse(tempBuffer);
        const sanitizedContent = DOMPurify.sanitize(renderedContent);
        if (textContainer) {
          textContainer.innerHTML = sanitizedContent;  // 追加最后一部分文本内容
        }
      }
  
      // 滚动到底部
      this.chatLog.scrollTop = this.chatLog.scrollHeight;
    }
  }

  //处理代码快内容
  private async formatCodeBlockHtmlFn(messageId:string):Promise<string | void>{
    const messageElement = document.getElementById(messageId) as HTMLDivElement;
    let textContainer = messageElement.querySelector('.text-content') as Element;
      const sanitizedContent = DOMPurify.sanitize(textContainer);
      const codeBlockRegex = /<pre><code class="language-(\w+)">([\s\S]*?)<\/code><\/pre>/g;
      const hasCodeBlock = codeBlockRegex.test(sanitizedContent);
      setTimeout(()=>{
        if(hasCodeBlock){
          const formattedContent = sanitizedContent.replace(
            codeBlockRegex,
            (match, lang, code) => {
              return `
              <div class="code-wrapper">
                <div class="code-header">
                  <span class="code-language">${lang}</span>
                  <button class="copy-button">复制</button>
                </div>
                <pre><code class="language-${lang}">${code}</code></pre>
              </div>
            `;
            }
          );
    
          textContainer.innerHTML = formattedContent;
    
          textContainer.querySelectorAll('.copy-button').forEach(button => {
            button.addEventListener('click', () => {
              const codeElement = button
                .closest('.code-wrapper')
                ?.querySelector('code');
              if (codeElement) {
                copyCodeToClipboard(codeElement);
                const originalText = button.textContent;
                button.textContent = '已复制!';
                setTimeout(() => {
                  button.textContent = originalText;
                }, 2000);
              }
            });
          });
        }

        // 滚动到底部
        this.chatLog.scrollTop = this.chatLog.scrollHeight;
      },100)
  }

  private async deleteSession(sessionId: string): Promise<void> {
    await this.sessionManager.deleteSession(sessionId);
    this.loadSessions();

    if (this.currentSession && this.currentSession.id === sessionId) {
      this.currentSession = null; // 清空当前会话
      this.clearChatLog();
      this.initDefaultChatLog();
    }
  }

  private async addMessage(content: string, className: string, returnId = false): Promise<string | void> {
    const messageElement = document.createElement('div');
    const messageId = `message-${Date.now()}`;  // 生成唯一的消息ID
    messageElement.id = messageId;  // 给消息元素设置ID
    messageElement.className = `message ${className}`;

    if (className === 'bot-message') {
      const renderedContent = await marked.parse(content);
      const sanitizedContent = DOMPurify.sanitize(renderedContent);

      const codeBlockRegex =
        /<pre><code class="language-(\w+)">([\s\S]*?)<\/code><\/pre>/g;
      const formattedContent = sanitizedContent.replace(
        codeBlockRegex,
        (match, lang, code) => {
          return `
          <div class="code-wrapper">
            <div class="code-header">
              <span class="code-language">${lang}</span>
              <button class="copy-button">复制</button>
            </div>
            <pre><code class="language-${lang}">${code}</code></pre>
          </div>
        `;
        }
      );

      messageElement.innerHTML = formattedContent;

      messageElement.querySelectorAll('.copy-button').forEach(button => {
        button.addEventListener('click', () => {
          const codeElement = button
            .closest('.code-wrapper')
            ?.querySelector('code');
          if (codeElement) {
            copyCodeToClipboard(codeElement);

            const originalText = button.textContent;
            button.textContent = '已复制!';
            setTimeout(() => {
              button.textContent = originalText;
            }, 2000);
          }
        });
      });
    } else {
      messageElement.textContent = content;
    }

    this.chatLog.appendChild(messageElement);
    this.chatLog.scrollTop = this.chatLog.scrollHeight;
    // 根据调用情况返回 messageId 或不返回
    if (returnId) {
      return messageId;
    }
  }

  private async loadSessions(): Promise<void> {
    const sessions = await this.sessionManager.getSessions();
    // console.log('Loaded sessions:', sessions,JSON.stringify(sessions));
    this.displaySessionList(sessions);
  }

  private displaySessionList(sessions: Session[]): void {
    if (!sessions || sessions.length === 0) {
      console.warn('No sessions available.');
      return;
    }

    const validSessions = sessions.filter(
      session => session && session.lastModified
    );
    const sortedSessions = validSessions.sort(
      (a, b) => b.lastModified - a.lastModified
    );

    this.sessionList.innerHTML = '';

    sortedSessions.forEach(session => {
      const sessionElement = document.createElement('div');
      sessionElement.className = 'session-item';
      sessionElement.dataset.sessionId = session.id;

      const nameSpan = document.createElement('span');
      nameSpan.className = 'session-name';
      nameSpan.textContent = this.truncateSessionName(session.name);
      sessionElement.appendChild(nameSpan);

      // 三个点按钮，默认隐藏
      const moreOptions = document.createElement('div');
      moreOptions.className = 'more-options';
      moreOptions.style.display = 'none'; // 默认隐藏

      const moreBtn = document.createElement('button');
      moreBtn.className = 'more-btn';
      moreBtn.textContent = '⋮'; // 三个点图标
      moreBtn.addEventListener('click', e => {
        e.stopPropagation(); // 阻止事件冒泡
        console.log('more-btn clicked'); // 调试：检查点击是否生效
        this.toggleDropdown(moreOptions, dropdownMenu); // 显示或隐藏弹窗
      });

      // 弹出菜单
      const dropdownMenu = document.createElement('div');
      dropdownMenu.className = 'dropdown-menu';
      dropdownMenu.style.display = 'none'; // 默认隐藏

      // 重命名选项
      const renameButton = document.createElement('button');
      renameButton.textContent = '重命名';
      renameButton.addEventListener('click', () => {
        this.handleRenameSession(session); // 处理重命名逻辑
      });

      // 删除选项
      const deleteButton = document.createElement('button');
      deleteButton.className = 'delete-btn';
      deleteButton.textContent = '删除';
      deleteButton.addEventListener('click', e => {
        e.stopPropagation();
        this.deleteSession(session.id);
      });

      dropdownMenu.appendChild(renameButton);
      dropdownMenu.appendChild(deleteButton);
      moreOptions.appendChild(moreBtn);
      moreOptions.appendChild(dropdownMenu);
      sessionElement.appendChild(moreOptions);

      // 悬停时显示三个点按钮
      sessionElement.addEventListener('mouseenter', () => {
        moreOptions.style.display = 'block';
      });

      // 点击会话条目时加载该会话
      sessionElement.addEventListener('click', (event: Event) => {
        event.stopPropagation();
        const renameNode = this.node.querySelector('.rename-input');//激活重命名取消关闭侧边栏
        !renameNode ? this.toggleSidebar() : null;//取消默认显示内容
        this.hideDefaultChatLog();//取消默认显示内容
        this.loadSession(session); // 恢复并确保此功能存在
      });

      // 动态应用渐变效果
      this.applyFadeEffect(nameSpan);

      this.sessionList.appendChild(sessionElement);
    });
  }

  private async renameSession(
    sessionId: string,
    newName: string
  ): Promise<void> {
    const session = await this.sessionManager.loadSession(sessionId);
    if (session) {
      session.name = newName;
      await this.sessionManager.saveSessionToFile(session);
      this.loadSessions(); // 重新加载会话列表，更新显示
    }
  }

  private async loadSession(session: Session): Promise<void> {
    this.currentSession = session;

    // 找到并移除之前选中的会话
    const previousActive = this.sessionList.querySelector('.active-session');
    if (previousActive) {
      previousActive.classList.remove('active-session');
    }

    // 为当前会话添加 active-session 类
    const currentActive = this.sessionList.querySelector(
      `[data-session-id="${session.id}"]`
    );
    if (currentActive) {
      currentActive.classList.add('active-session');
    }

    // 清除并加载新的聊天记录
    this.clearChatLog();
    await this.displayAllSessionMessages(session.messages);
  }

  private toggleDropdown(
    moreOptions: HTMLDivElement,
    dropdownMenu: HTMLDivElement
  ): void {
    const isVisible = dropdownMenu.style.display === 'block';

    // 关闭其他所有的弹窗
    this.closeAllDropdowns();

    // 如果当前菜单未显示，则显示该菜单
    if (!isVisible) {
      console.log('Showing dropdown');
      dropdownMenu.style.display = 'block';
      moreOptions.style.display = 'block'; // 确保包含按钮和菜单的容器可见
      document.addEventListener('click', this.handleOutsideClick);
    } else {
      console.log('Hiding dropdown');
      dropdownMenu.style.display = 'none';
      document.removeEventListener('click', this.handleOutsideClick);
    }
  }

  private handleOutsideClick = (event: MouseEvent): void => {
    const clickedElement = event.target as HTMLElement;

    // 如果点击的不是弹窗或者三个点按钮，则关闭所有弹窗
    if (
      !clickedElement.closest('.dropdown-menu') &&
      !clickedElement.closest('.more-btn')
    ) {
      this.closeAllDropdowns();
    }
  };

  private closeAllDropdowns(): void {
    const dropdowns = this.sessionList.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(dropdown => {
      (dropdown as HTMLElement).style.display = 'none';
    });
  }

  private handleRenameSession(session: Session): void {
    const sessionElement = this.sessionList.querySelector(
      `[data-session-id="${session.id}"]`
    );
    const nameSpan = sessionElement?.querySelector(
      '.session-name'
    ) as HTMLSpanElement;

    if (nameSpan) {
      // 创建一个输入框替换当前标题
      const input = document.createElement('input');
      input.type = 'text';
      input.value = session.name;
      input.className = 'rename-input';
      input.style.width = `${nameSpan.clientWidth}px`; // 根据现有名称的宽度设置输入框宽度

      nameSpan.replaceWith(input);
      input.focus();

      // 保存新的名称
      const saveNewName = async () => {
        const newName = input.value.trim();
        if (newName && newName !== session.name) {
          session.name = newName;
          await this.renameSession(session.id, newName); // 调用 renameSession 函数

          // 调用 loadSessions 重新加载会话列表并更新排序
          this.loadSessions();

          // 为重新加载的会话条目应用渐变效果
          this.sessionList.querySelectorAll('.session-name').forEach(span => {
            this.applyFadeEffect(span as HTMLSpanElement);
          });
        } else {
          // 如果名称没有改变，恢复原来的标题
          nameSpan.textContent = session.name;
          input.replaceWith(nameSpan);

          // 应用渐变效果
          this.applyFadeEffect(nameSpan);
        }
      };

      // 点击 Enter 键保存新名称
      input.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
          saveNewName();
        }
      });

      // 输入框失去焦点时保存新名称
      input.addEventListener('blur', () => {
        saveNewName();
      });
    }
  }

  // 渐变效果
  private applyFadeEffect(element: HTMLSpanElement): void {
    const textContent = element.textContent || '';
    if (textContent.length > 14) {
      // 例如字数限制为20
      element.classList.add('fade-effect'); // 添加渐变效果的CSS类
    } else {
      element.classList.remove('fade-effect'); // 如果没有超出字数，移除渐变效果
    }
  }

  private clearChatLog(): void {
    this.chatLog.innerHTML = '';
  }

  private async displayAllSessionMessages(messages: Message[]): Promise<void> {
    for (const message of messages) {
      await this.addMessage(
        message.content,
        message.role === 'user' ? 'user-message' : 'bot-message'
      );
    }
    this.chatLog.scrollTop = this.chatLog.scrollHeight;
  }

  private createNewSession(): void {
    this.clearChatLog();
    this.currentSession = null; // 清除当前会话
  }

  private truncateSessionName(input: string, maxLength: number = 20): string {
    return input.length > maxLength
      ? input.substring(0, maxLength - 3) + '...'
      : input;
  }

  private getLimitedContextMessages(): Message[] {
    return this.currentSession
      ? this.currentSession.messages.slice(-this.MAX_CONTEXT_MESSAGES)
      : [];
  }

  private toggleSidebar(): void {
    const sidebarClassHidden = this.sidebar.classList;
    const toggleSidebarBg = this.toggleSidebarBg.classList
    const hasClassSidebarHidden = this.toggleSidebarBg.className;
    if (hasClassSidebarHidden.indexOf("chat-bg-show") > -1) {
      sidebarClassHidden.toggle('sidebar-hidden');
      setTimeout(() => {
        toggleSidebarBg.toggle('chat-bg-show');
      }, 300);
    } else {
      toggleSidebarBg.toggle('chat-bg-show');
      setTimeout(() => {
        sidebarClassHidden.toggle('sidebar-hidden');
      }, 100);
    }
  }

  //获取课程信息--公开课程知识库
  private async getPublicPorjectDatas(): Promise<void> {
    const openid = localStorage.getItem('openid') || '';
    this.publicPorjectData = await this.apiService.getPublicPorjectDatas(openid);
  }

  //获取付费课程信息
  private async getUserCouresPorjectDatas(): Promise<void> {
    const openid = localStorage.getItem('openid') || '';
    this.useFetchPorjectData = await this.apiService.getUserCouresPorjectDatas(openid);
  }

  private showDefaultChatLog(): void {
    this.chatLogDefaultContent.style.display = "block";
  }

  private hideDefaultChatLog(): void {
    this.chatLogDefaultContent.style.display = "none";
  }

  private initDefaultChatLog(): void {
    this.showDefaultChatLog();
  }

  //初始化页面
  private initDefaultchatContainer(): void {
    this.chatContainer.style.display = "none";
  }

  //显示课程名称转换
  private formatStringFn(value: string,labelName?:formatStringInterface,valueName?:formatStringInterface): string {
    let datas: Array<PorjectItemInterface> = [];
    const porjectTypeValue = this.node.querySelector("input[name='porjectTypeName']:checked") as HTMLInputElement;
    if (porjectTypeValue) {
      datas = porjectTypeValue.value === '1' ? this.publicPorjectData : porjectTypeValue.value === '2' ? this.useFetchPorjectData : [];
    }
    const id = labelName?labelName:'id';
    const name = valueName?valueName:"name";
    return datas.length > 0 ? datas.filter(k => k[id] === value).map(k => k[name]).join("") : "";
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

  // MateGen知识库创建相关
  // 处理传入的 knowledgeId 为 URL 的情况
private async handleKnowledgeIdUrl(openai: OpenAI, courseNumber: string): Promise<string> {
  const knowledgeId = courseNumber;
  try {
    const response = await fetch(knowledgeId);
    if (!response.ok) {
      throw new Error('无法下载知识库 JSON 文件');
    }
    const knowledgeJson = await response.json();

    // 获取知识库名称
    const knowledgeBaseName = knowledgeId.split('/').pop()?.replace(/\.[^/.]+$/, '') || 'default_knowledge_base';

    // 检查是否已有同名知识库
    const existingStoreId = await this.getExistingVectorStoreId(openai, knowledgeBaseName);
    if (existingStoreId) {
      console.log(`已找到同名知识库，知识库ID为: ${existingStoreId}`);
      return existingStoreId;
    }

    // 创建知识库文件夹
    const knowledgeBaseFolderPath = await this.createKnowledgeBaseFolder(knowledgeBaseName);

    // 下载文档并保存到知识库文件夹
    await this.downloadKnowledgeDocuments(knowledgeJson, knowledgeBaseFolderPath);

    // 创建新的知识库
    const vectorStoreId = await this.createVectorStore(openai, knowledgeBaseName);

    // 上传文档到 OpenAI 文件系统并添加到知识库
    await this.uploadDocumentsToVectorStore(openai, knowledgeBaseFolderPath, vectorStoreId);

    // 更新知识库 ID
    console.log(`Assistant API 知识库ID已更新为: ${vectorStoreId}`);
    
    // 删除本地 JSON 文件和知识库文件夹
    await this.deleteKnowledgeBaseFolderAndJson(knowledgeBaseName);
    return vectorStoreId;
  } catch (error) {
    console.error('知识库创建过程中发生错误:', error);
    return ''; // 添加返回以处理错误情况
  }
}

  // 处理传入的 knowledgeId 为本地文件夹路径的情况
  private async handleLocalKnowledgeFolder(openai: OpenAI, courseNumber: string): Promise<string> {
  	const knowledgeId = courseNumber
    const knowledgeBaseName = knowledgeId.split('/').pop() || 'default_knowledge_base';

    // 检查是否已有同名知识库
    const existingStoreId = await this.getExistingVectorStoreId(openai, knowledgeBaseName);
    if (existingStoreId) {
      console.log(`已找到同名知识库，知识库ID为: ${existingStoreId}`);
      return existingStoreId;
    }

    // 创建新的知识库
    const vectorStoreId = await this.createVectorStore(openai, knowledgeBaseName);

    // 上传文档到 OpenAI 文件系统并添加到知识库
    await this.uploadDocumentsToVectorStore(openai, knowledgeId, vectorStoreId);

    // 更新知识库 ID
    console.log(`Assistant API 知识库ID已更新为: ${vectorStoreId}`);
    return vectorStoreId;
  }

  // 获取同名知识库的 ID
  private async getExistingVectorStoreId(openai: OpenAI, knowledgeBaseName: string): Promise<string | null> {
    try {
      const vectorStores = await openai.beta.vectorStores.list();
      const existingStore = vectorStores.data.find(store => store.name === knowledgeBaseName);
      return existingStore ? existingStore.id : null;
    } catch (error) {
      console.error('获取现有知识库列表时出错:', error);
      return null;
    }
  }

  // 创建新的知识库
  private async createVectorStore(openai: OpenAI, knowledgeBaseName: string): Promise<string> {
    try {
      const vectorStore = await openai.beta.vectorStores.create({
        name: knowledgeBaseName
      });
      return vectorStore.id;
    } catch (error) {
      throw new Error('创建新的知识库时出错:' + error);
    }
  }

  // 创建知识库文件夹
  private async createKnowledgeBaseFolder(knowledgeBaseName: string): Promise<string> {
    const knowledgeBaseFolderPath = `${this.KNOWLEDGE_BASE_FOLDER}/${knowledgeBaseName}`;
    console.log(`临时知识库文件夹地址: ${knowledgeBaseFolderPath}`)
    try {
      await this.contents.get(knowledgeBaseFolderPath);
    } catch (error) {
      await this.contents.save(knowledgeBaseFolderPath, {
        type: 'directory',
        format: 'text',
        content: ''
      });
    }
    return knowledgeBaseFolderPath;
  }
  
// 下载知识库文档并保存到本地
private async downloadKnowledgeDocuments(knowledgeJson: any, knowledgeBaseFolderPath: string): Promise<void> {
  for (const [docTitle, docUrl] of Object.entries(knowledgeJson)) {
    if (typeof docUrl !== 'string') {
      console.warn(`文档URL无效，跳过: ${docUrl}`);
      continue;
    }
    try {
      const docResponse = await fetch(docUrl);
      if (!docResponse.ok) {
        console.warn(`文档下载失败，跳过: ${docUrl}`);
        continue;
      }
      const docContent = await docResponse.text();
      const docExtension = docUrl.split('.').pop();
      const docPath = `${knowledgeBaseFolderPath}/${docTitle}.${docExtension}`;
      await this.contents.save(docPath, {
        type: 'file',
        format: 'text',
        content: docContent
      });
    } catch (error) {
      console.warn(`文档处理失败，跳过: ${docUrl}`);
    }
  }
}

  // 上传文档到 OpenAI 文件系统并添加到知识库
  private async uploadDocumentsToVectorStore(openai: OpenAI, folderPath: string, vectorStoreId: string): Promise<void> {
 console.warn(`文件上传失败，跳过: ${folderPath}`);
  }

  // 删除本地知识库文件夹和 JSON 文件
  private async deleteKnowledgeBaseFolderAndJson(knowledgeBaseName: string): Promise<void> {
    const knowledgeBaseFolderPath = `${this.KNOWLEDGE_BASE_FOLDER}/${knowledgeBaseName}`;
    try {
      await this.contents.delete(knowledgeBaseFolderPath);
      await this.contents.delete(`${this.KNOWLEDGE_BASE_FOLDER}/${knowledgeBaseName}.json`);
    } catch (error) {
      console.warn(`删除知识库文件夹或 JSON 文件时出错: ${knowledgeBaseFolderPath}`);
    }
  }


}
