import Taro from '@tarojs/taro';
import apiConfig from '../apiConfig';

// 网络请求拦截器
const interceptor = function (chain) {
  const requestParams = chain.requestParams;
  const { method, data, url } = requestParams;
  console.log("拦截器被调用");
  let token = Taro.getStorageSync('token'); // 拿到本地缓存中存的token
  if (!apiConfig.whiteList.includes(url) && (!token || token == "")) {
    Taro.switchTab({
      url: '/pages/mine/index' // 假设登录页面的路径是 /pages/mine
    });
    return Promise.reject('未登录');
  }

  requestParams.header = {
    ...requestParams.header,
    Authorization: 'Bearer ' + token // 将token添加到头部
  };

  return chain.proceed(requestParams).then(res => {
    return res;
  });
};

const request = async (method, url, params) => {
  let contentType = params?.data ? 'application/json' : 'application/x-www-form-urlencoded';
  if (params) contentType = params?.headers?.contentType || contentType;
  const option = {
    method,
    url: apiConfig.baseUrl + url,
    data: params && (params?.data || params?.params),
    header: {
      'content-type': contentType,
    }
  };
  Taro.showLoading({ title: '加载中' });
  try {
    const resp = await Taro.request(option);
    Taro.hideLoading();
    switch (resp?.statusCode) {
      case 200:
        return { success: true, data: resp.data };
      case 401:
        Taro.showToast({ title: '未授权，请登录', icon: 'none' });
        Taro.switchTab({ url: '/pages/mine/index' });
        return { success: false, message: '未授权，请登录' };
      case 403:
        Taro.showToast({ title: '拒绝访问', icon: 'none' });
        return { success: false, message: '拒绝访问' };
      case 404:
        Taro.showToast({ title: '请求地址出错', icon: 'none' });
        return { success: false, message: '请求地址出错' };
      case 500:
        Taro.showToast({ title: '服务器内部错误', icon: 'none' });
        return { success: false, message: '服务器内部错误' };
      case 503:
        Taro.showToast({ title: '服务不可用', icon: 'none' });
        return { success: false, message: '服务不可用' };
      default:
        Taro.showToast({ title: `连接出错 ${resp.statusCode}`, icon: 'none' });
        return { success: false, message: `连接出错 ${resp.statusCode}` };
    }
  } catch (error) {
    Taro.hideLoading();
    Taro.showToast({ title: '请求失败，请检查网络', icon: 'none' });
    console.error('请求接口出现问题', error);
    return { success: false, message: '请求失败，请检查网络' };
  }
};
Taro.addInterceptor(interceptor);
export default {
  get: (url, config) => {
    return request('GET', url, config);
  },
  post: (url, config) => {
    return request('POST', url, config);
  },
  put: (url, config) => {
    return request('PUT', url, config);
  },
  delete: (url, config) => {
    return request('DELETE', url, config);
  },
  patch: (url, config) => {
    return request('PATCH', url, config);
  },
};