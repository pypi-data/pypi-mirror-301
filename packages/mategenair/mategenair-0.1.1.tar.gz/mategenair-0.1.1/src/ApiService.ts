export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}
import { PorjectItemInterface} from './types'; 
import OpenAI from "openai";
export class ApiService {
  private backendUrl: string = 'http://mate.wsp2.cn';  
  private jwtToken: string = '';  
  private jwtExpiration: number = 0;  
  private knowledge_id: string = '';  
  private modelName: string = '';
  private mateGenApiKey: string = '';  // 添加 MateGen API KEY 字段

    private parseJwt(token: string): any {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
  }
  
  // 设置新的 knowledge_id
  public setKnowledgeId(knowledgeId: string): void {
    this.knowledge_id = knowledgeId;
    console.log(`知识库ID已更新为: ${this.knowledge_id}`);
  }  

  constructor(mateGenApiKey: string = '') {
    this.mateGenApiKey = mateGenApiKey;  // 在构造函数中接受 API KEY
  }
  // 检查当前 Token 是否过期
  public isTokenExpired(): boolean {
    const currentTime = Math.floor(Date.now() / 1000);  // 当前时间戳
    return this.jwtExpiration <= currentTime;
  }

  // 请求后端获取新的 JWT Token
  private async fetchNewToken(): Promise<void> {
    const response = await fetch(`${this.backendUrl}/generate-glm4-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    this.jwtToken = data.token;
    this.modelName = data.model_name;

    // 解码 JWT Token 以提取过期时间
    const decoded = this.parseJwt(this.jwtToken);
    this.jwtExpiration = decoded.exp;
  }
  

public async getBotReply(
  contextMessages: Message[],
  assistantIdOrCallback: string | ((message: string) => void),
  threadIdOrCallback?: string | ((message: string) => void),
  onStreamMessage?: (message: string) => void
): Promise<void> {
  try {
    if (this.mateGenApiKey && typeof assistantIdOrCallback === 'string' && typeof threadIdOrCallback === 'string') {
      // 使用 Assistant API
      const assistantId = assistantIdOrCallback;
      const threadId = threadIdOrCallback;

      // 创建 OpenAI 客户端
      const openai = new OpenAI({
        apiKey: this.mateGenApiKey,
        dangerouslyAllowBrowser: true
      });

      // 验证 assistantId 和 threadId
      if (!assistantId || !threadId) {
        throw new Error('assistantId 或 threadId 缺失，无法进行 Assistant API 响应');
      }

      // 提取 contextMessages 中最后一条用户消息
      const lastUserMessage = contextMessages
        .filter(message => message.role === 'user')
        .slice(-1)[0];

      if (lastUserMessage) {
        await openai.beta.threads.messages.create(threadId, {
          content: lastUserMessage.content,
          role: 'user'
        });
      }

      // 启用 Assistant API 流式调用
      openai.beta.threads.runs.stream(threadId, {
        assistant_id: assistantId
      })
        .on('textCreated', (text) => onStreamMessage!('\nMateGen：'))
        .on('textDelta', (textDelta, snapshot) => {
          if (textDelta?.value) {
            onStreamMessage!(textDelta.value);
          }
        })
        .on('toolCallCreated', (toolCall) => onStreamMessage!(`\n**正在调用${toolCall.type}...**\n\n`))
        .on('toolCallDelta', (toolCallDelta, snapshot) => {
          if (toolCallDelta.type === 'code_interpreter' && toolCallDelta.code_interpreter) {
            if (toolCallDelta.code_interpreter.input) {
              onStreamMessage!(toolCallDelta.code_interpreter.input);
            }
            if (toolCallDelta.code_interpreter.outputs) {
              onStreamMessage!("\noutput >\n");
              toolCallDelta.code_interpreter.outputs.forEach(output => {
                if (output.type === "logs") {
                  onStreamMessage!(`\n${output.logs}\n`);
                }
              });
            }
          }
        });
    } else {
      // 使用 GLM 模型
      const onStreamMessageCallback = typeof assistantIdOrCallback === 'function'
        ? assistantIdOrCallback
        : threadIdOrCallback as (message: string) => void;

      if (!this.jwtToken || this.isTokenExpired()) {
        await this.fetchNewToken();
      }
      const systemMessage: Message = {
	  role: 'system',
	  content: '你是MateGen，是由九天老师团队开发的智能编程和问答助手，底层模型未知。'
	};
	
	// 将 systemMessage 添加到 contextMessages 的开头
	const modifiedContextMessages = [systemMessage, ...contextMessages];


      const requestBody: any = {
        model: this.modelName,
        messages: modifiedContextMessages,
        stream: true
      };

      if (this.knowledge_id) {
        requestBody.tools = [
          {
            type: "retrieval",
            retrieval: {
              knowledge_id: this.knowledge_id,
              prompt_template: "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。\n不要复述问题，直接开始回答。"
            }
          }
        ];
      }

      const response = await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.jwtToken}`
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      // 处理流式响应
      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        let done = false;
        let accumulatedText = '';

        while (!done) {
          const { value, done: readerDone } = await reader.read();
          done = readerDone;

          const chunk = decoder.decode(value, { stream: true });
          accumulatedText += chunk;

          const lines = accumulatedText.split('\n');
          for (const line of lines) {
            if (line.startsWith('data:')) {
              const jsonData = line.replace('data: ', '');
              if(jsonData==='[DONE]'){return}
              try {
                const parsed = JSON.parse(jsonData);
                const messageChunk = parsed.choices[0].delta?.content;
                if (messageChunk) {
                  onStreamMessageCallback(messageChunk);
                }
              } catch (error) {
                console.error('Error parsing stream data:', error);
              }
            }
          }

          accumulatedText = lines[lines.length - 1];
        }
      }
    }
  } catch (error) {
    console.error('Error fetching bot reply:', error);
    throw error;
  }
}


  // 获取机器人回复
  public async getBotReplyNoStream(contextMessages: Message[]): Promise<string> {
    try {
      // 检查 JWT Token 是否过期，若过期则刷新
      if (!this.jwtToken || this.isTokenExpired()) {
        await this.fetchNewToken();
      }

      // 构建请求体的基础部分
      const requestBody: any = {
        model: 'glm-4-flash',
        messages: contextMessages,
      };

      // 如果有 knowledge_id，则添加 tools 参数
      if (this.knowledge_id) {
        requestBody.tools = [
          {
            type: "retrieval",
            retrieval: {
              knowledge_id: this.knowledge_id,
              prompt_template: "从文档\n\"\"\"\n{{knowledge}}\n\"\"\"\n中找问题\n\"\"\"\n{{question}}\n\"\"\"\n的答案，找到答案就仅使用文档语句回答问题，找不到答案就用自身知识回答并且告诉用户该信息不是来自文档。\n不要复述问题，直接开始回答。"
            }
          }
        ];
      }

      const response = await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.jwtToken}`  // 使用 JWT Token
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      return data.choices[0].message.content;
    } catch (error) {
      console.error('Error fetching bot reply:', error);
      throw error;
    }
  }
  
  // 获取当前 knowledge_id 的课程编号
  public async getCourseNumberByKnowledgeId(): Promise<string> {
    if (!this.knowledge_id) return '未设置知识库';

    const response = await fetch('http://mate.wsp2.cn/knowledge-to-course', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ knowledge_id: this.knowledge_id })
    });

    if (response.ok) {
      const data = await response.json();
      return data.course_number || '未设置知识库';
    } else {
      return '未设置知识库';
    }
  }

  // 获取公开课信息
  public async getPublicPorjectDatas(openid: string): Promise<Array<PorjectItemInterface>> {
    // 如果是 Assistant API 模式，发起请求以获取课程下载地址
    const url = this.mateGenApiKey
      ? `${this.backendUrl}/fetch-assistant-public-courses`
      : `${this.backendUrl}/fetch-public-courses`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "openid": openid
      })
    });

    const data = await response.json();
    let datas = [];
    if (response.ok) {
      datas = data && data.courses && data.courses.length > 0 ? data.courses : [];
    } else {
      datas = [];
    }

    console.log("data", data);
    return datas;
  }

  // 获取付费课程信息
  public async getUserCouresPorjectDatas(openid: string): Promise<Array<PorjectItemInterface>> {
    const url = this.mateGenApiKey
      ? `${this.backendUrl}/get-assistant-user-courses`
      : `${this.backendUrl}/get-user-courses`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "openid": openid
      })
    });
    const data = await response.json();
    let datas = [];
    if (response.ok) {
      datas = data && data.courses && data.courses.length > 0 ? data.courses : [];
    } else {
      datas = [];
    }

    return datas;
  }

  // 获取自动课程消息回复
  public  async getRestNew(typeName:String): Promise<string> {
    const chatbotDefaultEdit = "打开MateGen并登陆之后，打开任意ipy文件，选择某个cell，并点击cell输入栏最右侧小灯泡按钮，即可开启自动编程功能哦～MateGen提供的自动编程功能包括：\n\n 1.AI编程：仅需一句话，即可全自动创建Python代码，点击小灯泡按钮并选择“AI自动编程”，在输入框内输入编程需求，比如“请帮我编写一个K-Means聚类算法”，则可自动创建完整的Python代码哦；\n\n 2.代码优化；点击小灯泡按钮并选择“代码优化”，即可让MateGen为你的代码进行优化；\n\n 3.代码注释：点击小灯泡按钮并选择“代码注释”，即可让MateGen为你的代码进行逐行优化；";
    const chatbotDefaultResponse = "在最下方输入栏左侧，点击文件夹按钮，即可设置问答的课程知识库哦～只需输入课程编号，即可将MateGen的知识库设置为对应的课程内容哦，接下来小伙伴就可以询问任何这门课程里面的技术内容啦～并且在一次会话中可以随时切换课程知识库哦，祝小伙伴学习愉快！"
    return new Promise(resolve => setTimeout(resolve, 2000)).then(()=>{
      return typeName==='edit'?chatbotDefaultEdit:typeName==='resp'?chatbotDefaultResponse:'';
    });
  }
}