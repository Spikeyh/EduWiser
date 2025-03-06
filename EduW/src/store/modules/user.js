import { createSlice } from "@reduxjs/toolkit";
import Taro from '@tarojs/taro';
import apiConfig from "../../apiConfig";
import Request from "../../services/httpService"

const userStore = createSlice({
    name: 'user',
    initialState: {
        token: "",
        nickname: ""
    },
    reducers: {
        SetStorage: (state, action) => {
            state.token = action.payload;
            Taro.setStorage({
                key: 'token',
                data: action.payload
            });
        },
        RemoveStorage: (state) => {
            state.token = "";
            Taro.removeStorage({
                key: 'token'
            });
        },
        SetNickname: (state, action) => {
            state.nickname = action.payload;
        }
    }
});

const { SetStorage, SetNickname } = userStore.actions;
const userReducer = userStore.reducer;

const fetchLogin = (e) => {
    return async (dispatch) => {
        const { code, encryptedData, iv } = e.detail;
        const response = await Request.post('/wx/login/auth', {data: {code,encryptedData,iv}});
        if (response.success) {
            dispatch(SetStorage(response.cookies[0]));
            Taro.showToast({ title: '登录成功'});
            console.log('登录请求成功', response.data);
        } else {
            // Taro.showToast({ title: '登录失败', icon: 'none' });
            console.log('登录请求失败');
        }
    }
}

const getNickname = (e) => {
    return async (dispatch) => {
        const response = await Request.post('/api/user');
        if (response.success) {
            dispatch(SetNickname(response.data.nickname));
        } else {
            console.log(response.message); // 处理错误信息
        }
    }
}

export { SetStorage, fetchLogin, getNickname }
export default userReducer