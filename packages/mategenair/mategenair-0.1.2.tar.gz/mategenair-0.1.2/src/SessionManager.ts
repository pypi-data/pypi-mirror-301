import { Contents } from '@jupyterlab/services';  // 这里引入 Contents 接口

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface Session {
  id: string;
  name: string;
  mg_id?: string;  // 新增 mg_id 字段，默认为空字符串，可以省略
  messages: Message[];  // 将原本的 content 更改为 messages
  lastModified: number;
}

export class SessionManager {
  private contents: Contents.IManager;  // 使用 IManager 进行文件管理
  private readonly SESSIONS_FOLDER = 'MateGen_sessions';  // 使用 MateGen_sessions 文件夹

  constructor(contents: Contents.IManager) {
    this.contents = contents;
    this.ensureSessionsFolderExists();  // 确保文件夹存在
  }

  // 确保会话文件夹存在
  private async ensureSessionsFolderExists(): Promise<void> {
    try {
      // 检查是否已经存在 MateGen_sessions 文件夹
      await this.contents.get(this.SESSIONS_FOLDER);
    } catch (error) {
      // 如果文件夹不存在，则创建它
      await this.contents.save(this.SESSIONS_FOLDER, {
        type: 'directory',
        format: 'json',
        content: ''
      });
    }
  }

  // 只有当用户发送第一条消息时，才创建会话文件
  async createNewSessionOnFirstMessage(userMessage: Message): Promise<Session> {
    const session: Session = {
      id: this.generateUniqueId(),
      name: this.truncateMessage(userMessage.content),  // 使用第一条消息作为会话名
      mg_id: '',  // 新增字段，默认值为空字符串
      messages: [userMessage],  // 将第一条消息加入会话
      lastModified: Date.now()
    };
    await this.saveSessionToFile(session);  // 保存到文件
    return session;
  }

  // 删除会话
  async deleteSession(sessionId: string): Promise<void> {
    const filePath = `${this.SESSIONS_FOLDER}/${sessionId}.json`;
    try {
      await this.contents.delete(filePath);
    } catch (error) {
      console.error(`Error deleting session: ${sessionId}`, error);
    }
  }

  // 实时保存会话到文件
  async saveSessionToFile(session: Session): Promise<void> {
    session.lastModified = Date.now();
    const fileName = `${session.id}.json`;
    const filePath = `${this.SESSIONS_FOLDER}/${fileName}`;
    const sessionContent = JSON.stringify(session, null, 2);
    console.log(sessionContent)

    try {
      const savedModel = await this.contents.save(filePath, {
        type: 'file',
        format: 'text',
        content: sessionContent, 
      });
      console.log('Session saved successfully:', filePath);
      console.log('Saved model:', savedModel);  // 打印返回的模型，检查元数据
    // 调试：保存文件后立即尝试读取文件，验证是否成功更新
    const sessionData = await this.contents.get(filePath, { format: 'text', content: true });
    console.log('Session data after saving:', sessionData);

    if (sessionData && sessionData.content) {
      const parsedContent = JSON.parse(sessionData.content);
      console.log('Parsed session content:', parsedContent);
    } else {
      console.warn('Session content is null or invalid after saving.');
    }      
    } catch (error) {
      console.error('Error saving session to file:', error);
    }
  }

  // 读取所有会话
	async getSessions(): Promise<Session[]> {
	  const sessions: Session[] = [];
	  try {
	    const sessionFiles = await this.contents.get(this.SESSIONS_FOLDER);
	
	    if (sessionFiles.type === 'directory') {
	      for (const file of sessionFiles.content) {
	        if (file.type === 'file') {
	          try {
	            const sessionData = await this.contents.get(`${this.SESSIONS_FOLDER}/${file.name}`, { format: 'text', content: true });
	
	            if (sessionData && sessionData.content) {
	              const session: Session = JSON.parse(sessionData.content);
	
	              // 确保每个会话都有 mg_id 字段
	              if (!session.mg_id) {
	                session.mg_id = '';
	              }
	
	              sessions.push(session);
	            }
	          } catch (fileError) {
	            console.error(`Error reading session file: ${file.name}`, fileError);
	          }
	        }
	      }
	    }
	  } catch (error) {
	    console.error('Error fetching session files:', error);
	  }
	
	  return sessions;
	}

  // 读取单个会话
	async loadSession(sessionId: string): Promise<Session | null> {
	  try {
	    const filePath = `${this.SESSIONS_FOLDER}/${sessionId}.json`;
	    const sessionData = await this.contents.get(filePath, { format: 'text', content: true });
	    const session = JSON.parse(sessionData.content) as Session;
	
	    // 如果会话中没有 mg_id 字段，默认给它设置为空字符串
	    if (!session.mg_id) {
	      session.mg_id = '';
	    }
	
	    return session;
	  } catch (error) {
	    console.error('Error loading session:', error);
	    return null;
	  }
	}

  // 生成唯一的会话ID
  private generateUniqueId(): string {
    return 'session-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }

  // 裁剪消息，作为会话名称
  private truncateMessage(message: string, maxLength: number = 20): string {
    return message.length > maxLength ? message.substring(0, maxLength - 3) + '...' : message;
  }
}