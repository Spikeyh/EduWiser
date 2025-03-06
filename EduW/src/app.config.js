export default {
  pages: [
    'pages/home/index',
    'pages/plan/index',
    'pages/news/index',
    'pages/mine/index',
    'pages/login/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: 'WeChat',
    navigationBarTextStyle: 'black'
  },
  tabBar: {
    list: [
      {
        pagePath: 'pages/home/index',
        text: '主页',
        iconPath: './assets/icons/home.png',
        selectedIconPath: './assets/icons/home.png'
      },
      {
        pagePath: 'pages/plan/index',
        text: '方案',
        iconPath: './assets/icons/plan.png',
        selectedIconPath: './assets/icons/plan.png'
      },
      {
        pagePath: 'pages/news/index',
        text: '资讯',
        iconPath: './assets/icons/news.png',
        selectedIconPath: './assets/icons/news.png'
      },
      {
        pagePath: 'pages/mine/index',
        text: '我的',
        iconPath: './assets/icons/mine.png',
        selectedIconPath: './assets/icons/mine.png'
      }
    ],
    color: '#8a8a8a',
    selectedColor: '#1c1c1c',
    backgroundColor: '#ffffff',
    borderStyle: 'black'
  }
};
