export class Circle {
  pos: any;
  radius: number;
  color: string;
  active: number;

  constructor(pos: any, rad: number, color: string) {
    this.pos = pos;
    this.radius = rad * 0.7;
    this.color = color;
    this.active = 0;
  }

  draw(ctx: CanvasRenderingContext2D | null) {
    if (!this.active || !ctx) return;
    ctx.beginPath();
    ctx.arc(this.pos.x, this.pos.y, this.radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = `rgba(156,217,249,${this.active})`;
    ctx.fill();
  }
}
