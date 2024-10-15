import { Circle } from './Circle';
import { TweenLite, Circ } from 'gsap';

let points: any[] = [];
let target = { x: 0, y: 0 };
let width: number, height: number, ctx: CanvasRenderingContext2D | null = null;
let canvas: HTMLCanvasElement | null = null;
let largeHeader: HTMLElement | null = null;
let animateHeader = true;

// 初始化 header 和 canvas
export function initHeader(): void {
	console.log('initHeader called');  // 添加日志
  canvas = document.getElementById('demo-canvas') as HTMLCanvasElement;
  if (!canvas) {
    console.error('Canvas element not found!');
  } else {
    console.log('Canvas element found:', canvas);
  }

  ctx = canvas.getContext('2d');
  if (!ctx) {
    console.error('Canvas context (ctx) not available!');
  } else {
    console.log('Canvas context initialized successfully');
  }
	
  // 获取 content 元素
  const content = document.querySelector('.content') as HTMLElement;
  if (content && content.parentElement) {
    const contentWidth = content.clientWidth;
    const contentHeight = content.clientHeight;

    // 初始化时调用 resizeCanvas，生成点并设置 canvas 尺寸
    console.log('Initial content size:', contentWidth, contentHeight);  // 添加日志
    resizeCanvas(contentWidth, contentHeight);

    // 使用 ResizeObserver 监听父容器大小的变化
    const resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        if (entry.contentRect) {
          const parentWidth = entry.contentRect.width;
          const parentHeight = entry.contentRect.height<500?500:entry.contentRect.height;
          console.log('Resizing canvas to:', parentWidth, parentHeight);  // 添加日志

          // 每次变化时调用 resizeCanvas 重新生成点并调整大小
          resizeCanvas(parentWidth, parentHeight);
        }
      }
    });

    // 监听 content 的父容器大小变化
       resizeObserver.observe(content.parentElement);
  } else {
    console.error('Content element not found!');  // 错误日志
  }

  // 添加事件监听器 (鼠标移动、滚动等)
  addListeners();

  // 初始化动画效果
  initAnimation();
}

// 重置 canvas 大小并重新生成点
export function resizeCanvas(contentWidth: number, contentHeight: number): void {
	console.log('resizeCanvas called with:', contentWidth, contentHeight);  // 添加日志
  // 更新全局宽度和高度
  width = contentWidth;
  height = contentHeight;

  // 更新 largeHeader 的高度
  if (largeHeader) {
    largeHeader.style.height = `${height}px`;
    console.log('Updated largeHeader height:', height);  // 添加日志
  }

  // 更新 canvas 的宽度和高度
  if (canvas) {
    canvas.width = width;
    canvas.height = height;
    console.log('Updated canvas size:', width, height);  // 添加日志

    // 重新初始化点的坐标
    points = [];
    createPoints();
    console.log('Points created:', points.length);  // 添加日志

    // 重新为每个点计算最近邻居
    for (let i = 0; i < points.length; i++) {
      const p1 = points[i];
      const closest: any[] = [];

      // 遍历其他点，找到最近的5个点
      for (let j = 0; j < points.length; j++) {
        const p2 = points[j];
        if (p1 !== p2) {
          const dist = getDistance(p1, p2);
          if (closest.length < 5) {
            closest.push(p2);
          } else {
            let maxDist = getDistance(p1, closest[0]);
            let maxIndex = 0;
            for (let k = 1; k < closest.length; k++) {
              const distClosest = getDistance(p1, closest[k]);
              if (distClosest > maxDist) {
                maxDist = distClosest;
                maxIndex = k;
              }
            }
            if (dist < maxDist) {
              closest[maxIndex] = p2;
            }
          }
        }
      }
      p1.closest = closest;

      // 为每个点重新创建 circle 对象
      if (!p1.circle) {
        p1.circle = new Circle(p1, 2 + Math.random() * 5, 'rgba(255,255,255,0.6)');
      }
    }

    // 重新绘制动画
    initAnimation();
  } else {
    console.error('Canvas not found!');  // 错误日志
  }
}

// 创建点
function createPoints() {
  points = [];
  for (let x = 0; x < width; x = x + width / 20) {
    for (let y = 0; y < height; y = y + height / 20) {
      const px = x + Math.random() * width / 20;
      const py = y + Math.random() * height / 20;
      const p = { x: px, originX: px, y: py, originY: py };
      points.push(p);
    }
  }
}

// 动画初始化
export function initAnimation(): void {
	console.log('initAnimation called');  // 添加日志
  animate();
  for (let i in points) {
    shiftPoint(points[i]);
  }
}

// 动画循环
function animate(): void {
  if (animateHeader && ctx) {
    ctx.clearRect(0, 0, width, height);
    for (let i in points) {
      const point = points[i];
      const distance = Math.abs(getDistance(target, point));

      // 动态调整点的透明度
      if (distance < 4000) {
        point.active = 0.3;
        if (point.circle) {
          point.circle.active = 0.6;
        }
      } else if (distance < 20000) {
        point.active = 0.1;
        if (point.circle) {
          point.circle.active = 0.3;
        }
      } else if (distance < 40000) {
        point.active = 0.02;
        if (point.circle) {
          point.circle.active = 0.1;
        }
      } else {
        point.active = 0;
        if (point.circle) {
          point.circle.active = 0;
        }
      }

      // 绘制线条和圆圈
      if (Array.isArray(point.closest)) {
        drawLines(point);
      }
      if (point.circle) {
        point.circle.draw(ctx);
      }
    }
  }else {
  console.log('Animation stopped or no canvas context available');  // 添加日志
  }
  requestAnimationFrame(animate);
}

// 鼠标移动事件
function mouseMove(e: MouseEvent): void {
  let posx = 0;
  let posy = 0;

  const content = document.querySelector('.content') as HTMLElement;
  if (!content) {
    console.error("Content 元素未找到！");
    return;
  }

  const rect = content.getBoundingClientRect();

  if (e.pageX || e.pageY) {
    posx = e.pageX - rect.left;
    posy = e.pageY - rect.top;
  } else if (e.clientX || e.clientY) {
    posx = e.clientX - rect.left;
    posy = e.clientY - rect.top;
  }

  target.x = posx;
  target.y = posy;
}

// 事件监听器
export function addListeners(): void {
  const content = document.querySelector('.content') as HTMLElement;

  if (!content) {
    console.error("Content 元素未找到！");
    return;
  }

  if (!('ontouchstart' in window)) {
    content.addEventListener('mousemove', mouseMove);
  }

  content.addEventListener('scroll', scrollCheck);
}

// 滚动事件
function scrollCheck(): void {
  animateHeader = document.body.scrollTop <= height;
}

// 点移动动画
function shiftPoint(p: any): void {
  TweenLite.to(p, 1 + 1 * Math.random(), {
    x: p.originX - 50 + Math.random() * 100,
    y: p.originY - 50 + Math.random() * 100,
    ease: Circ.easeInOut,
    onComplete: () => shiftPoint(p)
  });
}

// 绘制线条
function drawLines(p: any): void {
  if (!p.active || !ctx) return;
  ctx.lineWidth = 0.7;  // 线条更细
  for (let i in p.closest) {
    const closestPoint = p.closest[i];
    if (closestPoint) {
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(closestPoint.x, closestPoint.y);
      ctx.strokeStyle = `rgba(156,217,249,${p.active})`;
      ctx.stroke();
    }
  }
}

// 计算两点之间的距离
function getDistance(p1: any, p2: any): number {
  return Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2);
}
