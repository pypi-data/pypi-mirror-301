import { reloadIcon } from './icons';  // 引入图标
import { initHeader, addListeners, initAnimation, resizeCanvas } from './animation';

export class LoginManager {
    private loginContainer: HTMLDivElement;
    private onLoginSuccess: (token: string) => void;
    private qrcodeContainer: HTMLDivElement;
    private sessionId: string | null = null;

    constructor(loginContainer: HTMLDivElement, onLoginSuccess: (token: string) => void) {
        this.loginContainer = loginContainer;
        this.onLoginSuccess = onLoginSuccess;
        
        // 添加 CSS 类
        this.loginContainer.classList.add('login-container');

        this.loginContainer.innerHTML = `
		<div class="container demo-1 login-container-content com-scroll">
		    <div class="content login-container-box">
		        <canvas id="demo-canvas"></canvas>
		        <!-- 欢迎页面内容 -->
		        <div id="large-header" class="large-header">
		            <h2 class="sub-title">欢迎使用</h2>  <!-- 添加副标题 -->
		            <h1 class="main-title">MateGen</h1>  <!-- 主标题 -->
		            <p class="description">你的专属7*24小时智能助教</p>  <!-- 说明文字 -->
		            <button class="action-btn">立即使用</button> <!-- 按钮 -->
		        </div>
		        
		        <!-- 登录页面内容 -->
				<div id="login-page"> <!-- 初始位置在屏幕外 -->
				    <div class="login-content">
				        <h2 class="login-title">微信扫码登录</h2>
				        <div id="qrcode"></div>
				        <p class="login-description">扫码关注公众号<span class="qr_space"> 赋范空间 </span>完成登录</p>
				        <!-- 添加返回按钮 -->
				        <button class="back-btn">← Back</button>
				    </div>
				</div>
		    </div>
		</div>
        `;

        this.qrcodeContainer = this.loginContainer.querySelector('#qrcode') as HTMLDivElement;

        window.addEventListener('message', this.handleLoginMessage.bind(this), false);

        // 页面加载时检查 JWT 是否存在
        this.checkLoginStatusOnLoad();
        
    // 加入 setTimeout 确保 DOM 加载完成
    setTimeout(() => {
        console.log('DOM 加载完成，开始初始化动画');
        this.runAnimation();

        // 确保 DOM 加载完后再绑定事件监听
        this.addEventListeners();    
    }, 500);  // 0.5秒的延迟，确保 DOM 元素加载
}
    
	// 为按钮添加事件监听
	private addEventListeners(): void {
	    const actionBtn = document.querySelector('.action-btn');
	    const backBtn = document.querySelector('.back-btn');
	    const largeHeader = document.querySelector('.large-header');
	    const loginPage = document.getElementById('login-page');
	
	    // Debugging: Log elements to check if they're correctly selected
	    console.log("actionBtn:", actionBtn);
	    console.log("backBtn:", backBtn);
	    console.log("largeHeader:", largeHeader);
	    console.log("loginPage:", loginPage);
	
	    if (actionBtn && backBtn && largeHeader && loginPage) {
	        // 点击 "立即使用" 按钮时，滑动切换到登录页面
	        actionBtn.addEventListener('click', () => {
	            largeHeader.classList.add('slide-out');  // 欢迎页面滑出
	            loginPage.classList.add('slide-in');    // 登录页面滑入
                this.generateQRCode();//获取二维码
	        });
	
	        // 点击 "返回" 按钮时，滑动切换回欢迎页面
	        backBtn.addEventListener('click', () => {
	            largeHeader.classList.remove('slide-out'); // 欢迎页面滑回
	            loginPage.classList.remove('slide-in');    // 登录页面滑出
	        });
	    } else {
	        console.error("未找到页面元素，事件监听器无法绑定。");
	    }
	}
    

    // 检查 localStorage 中是否有有效的 JWT
  // 修改这个方法，使其返回一个布尔值表示是否已登录
  public checkLoginStatusOnLoad(): boolean {
    const token = localStorage.getItem('auth_token');

    if (token && !this.isTokenExpired(token)) {
      // JWT 有效，自动登录
      this.onLoginSuccess(token);
      return true;
    } else {
      // JWT 无效或不存在，显示扫码界面
      console.log('JWT 不存在或已过期，显示扫码界面');
      this.showLoginInterface();
      return false;
    }
  }

    // 检查 JWT 是否过期
    private isTokenExpired(token: string): boolean {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expiry = payload.exp * 1000; // 转换为毫秒
        return Date.now() > expiry;
    }

    public showLoginInterface(): void {
        console.log('Showing login interface');
        this.loginContainer.style.display = 'block';
        this.generateQRCode();
    }

    private async generateQRCode(): Promise<void> {
        try {
            console.log('Generating QR code...');

            // 清空之前的二维码容器
            this.qrcodeContainer.innerHTML = '';

            // 设置占位符，等待二维码生成
            const placeholder = document.createElement('div');
            placeholder.classList.add('placeholder');
            placeholder.innerText = '加载中...';
            this.qrcodeContainer.appendChild(placeholder);

            // 调用后端 API 获取二维码数据
            const response = await fetch('http://mate.wsp2.cn/get-wechat-qrcode', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
            });

            const data = await response.json();

            // 创建二维码图片
            const qrcodeImg = document.createElement('img');
            qrcodeImg.src = data.qrcodeUrl;
            qrcodeImg.alt = 'Login QR Code';
            qrcodeImg.classList.add('qrcode-image');

            // 平滑地替换占位符为二维码图片
            this.qrcodeContainer.replaceChild(qrcodeImg, placeholder);

            this.sessionId = data.session_id;
            console.log('QR code generated and displayed');

            this.pollLoginStatus();

            // 设置二维码过期处理
            setTimeout(() => {
                this.handleQRCodeExpired();
            }, 120000);

        } catch (error) {
            console.error('Error generating QR code:', error);
        }
    }
    
 private handleQRCodeExpired(): void {
      console.log('二维码已过期，请点击刷新二维码');

      // 清空二维码区域，显示一个可点击的占位符
      this.qrcodeContainer.innerHTML = '';

      const refreshPlaceholder = document.createElement('div');
      refreshPlaceholder.classList.add('refresh-placeholder');
      refreshPlaceholder.style.width = '100px';  // 设置占位符大小
      refreshPlaceholder.style.height = '100px';
      refreshPlaceholder.style.cursor = 'pointer'; // 鼠标移上去变成手型
      refreshPlaceholder.style.display = 'flex'; // 使用 flex 布局来居中图标
      refreshPlaceholder.style.justifyContent = 'center';
      refreshPlaceholder.style.alignItems = 'center';

      // 使用 LabIcon 将 SVG 图标插入到占位符中
      const iconElement = reloadIcon.element({
          container: refreshPlaceholder,
      });

      iconElement.style.width = '100%';  // 确保图标充满容器
      iconElement.style.height = '100%';
      iconElement.style.objectFit = 'contain'; // 保持图标的比例

      // 点击占位符重新生成二维码
      refreshPlaceholder.onclick = () => {
          refreshPlaceholder.style.transform = 'scale(0.95)'; // 点击时的按下效果
          setTimeout(() => {
              refreshPlaceholder.style.transform = ''; // 恢复原状
              this.generateQRCode(); // 生成新二维码
          }, 100);
      };

      this.qrcodeContainer.appendChild(refreshPlaceholder);
  }



    private async pollLoginStatus(): Promise<void> {
        const checkLoginStatus = async () => {
            try {
                if (!this.sessionId) {
                    throw new Error('Session ID is missing');
                }

                // console.log('Checking login status with session ID:', this.sessionId);

                const response = await fetch(`http://mate.wsp2.cn/check-login-status?session_id=${this.sessionId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    mode: 'cors',
                });

                const data = await response.json();
                if (data.logged_in && data.token) {
                    console.log('登录成功！');

                    // 存储 token 到 localStorage
                    localStorage.setItem('auth_token', data.token);
                    
                    // 如果后端返回了 openid，也可以存储或处理 openid
                    if (data.openid) {
                        console.log('获取到 openid:', data.openid);
                        localStorage.setItem('openid', data.openid);  // 存储 openid 到 localStorage
                    }

                    this.onLoginSuccess(data.token);
                    return;
                } else {
                    setTimeout(checkLoginStatus, 2000);
                }
            } catch (error) {
                console.error('Error checking login status:', error);
                setTimeout(checkLoginStatus, 2000);
            }
        };

        checkLoginStatus();
    }


    private handleLoginMessage(event: MessageEvent): void {
        // console.log('Received message:', event);
        if (event.data && event.data.type === 'login_success' && event.data.token) {
            localStorage.setItem('auth_token', event.data.token); // 保存 JWT
            this.onLoginSuccess(event.data.token);
        }
    }

    public hideLoginInterface(): void {
        this.loginContainer.style.display = 'none';
    }
    
  // 处理窗口大小变化时的逻辑
  public onResize(): void {
    console.log('捕捉到窗口的调整');
    const content = document.querySelector('.content') as HTMLElement;
	if (content) {
	  const contentWidth = content.clientWidth;
	  const contentHeight = content.clientHeight;
	  resizeCanvas(contentWidth, contentHeight);  // 调用 resizeCanvas 函数来调整大小
	}
  }

  // 初始化动画效果
  private runAnimation(): void {
    initHeader();
    addListeners();
    initAnimation();
  }

  // 显示头部组件
  public show(): void {
    this.loginContainer.style.display = 'block';
  }

  // 隐藏头部组件
  public hide(): void {
    this.loginContainer.style.display = 'none';
  }
}
