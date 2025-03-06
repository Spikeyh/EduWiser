import React from 'react';
import { View, Text, Button, Image } from '@tarojs/components';
import Taro from '@tarojs/taro';
import "./index.scss"
const Mine = () => {
  // const dispatch = useDispatch(); // 使用 dispatch 调用异步 action
  const src = "";
  const alt = "头像";
  // 点击事件
  const handleLoginClick = () => {
    // dispatch(fetchLogin()); // 触发异步登录
    console.log("click");
    Taro.navigateTo({url: '/pages/login/index'});
  };
  return (
    <View className="mine">
      <View className='login-card' onClick={handleLoginClick}>
        <View className="avatar-container">
          <Image className="avatar" src={src} alt={alt} />
        </View>
        <Text className='login-font'>登录/注册1</Text>
      </View>
      <View className='setting-card'>hello world</View>
    </View>
  );
};

export default Mine;
