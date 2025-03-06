import React from 'react';
import { View, Text, Button, Image } from '@tarojs/components';
import Taro from '@tarojs/taro';
import './index.scss';
import { fetchLogin, getNickname } from "../../store/modules/user";
import { useDispatch, useSelector } from 'react-redux';
const Login = () =>{
    const dispatch = useDispatch(); // 使用 dispatch 调用异步 action
    // 点击事件
    const onLoginClick = (e) => {
        dispatch(fetchLogin(e)); // 触发异步登录
    };
    const onClick = () => {
        dispatch(getNickname()); // 触发获取用户名
    }
    const nickname = useSelector((state) => state.user.nickname);
    const [userInfo, setUserInfo] = React.useState("");
    React.useEffect(() => {
        setUserInfo(nickname);
    }, [nickname]);
    return (
        <View className='login'>
            <Button className='login-btn' openType='getPhoneNumber' onGetPhoneNumber={onLoginClick}>手机号一键登录</Button>
            <Button className='login-btn' onClick={onClick}>测试，获取用户名</Button>
            <View>当前用户是：{userInfo}</View>
        </View>
    );
};
export default Login;