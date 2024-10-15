import { LabIcon } from '@jupyterlab/ui-components';
import reloadIconSvg from '../style/image/qr_reload.svg';  // 确保路径和文件存在

export const reloadIcon = new LabIcon({
  name: 'your-project:reload',
  svgstr: reloadIconSvg.replace(/%/g,'%25')
});

// export const topIcon = require('../style/image/qr_top.png');
// export const bottomIcon = require('../style/image/qr_bottom.png');
export const mategenIcon = require('../style/image/MateGenAir.svg');