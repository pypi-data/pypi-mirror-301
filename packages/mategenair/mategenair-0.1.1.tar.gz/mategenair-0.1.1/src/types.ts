export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface Session {
  id: string;
  name: string;
  mg_id?: string; // 新增 mg_id 字段，可能为 null，因此使用可选属性
  messages: Message[];
  lastModified: number;  // 使用时间戳记录最后修改时间
}

export interface PorjectItemInterface{
  id:string,
  name:string
}

export enum formatStringInterface{
  id="id",
  name="name"
}
