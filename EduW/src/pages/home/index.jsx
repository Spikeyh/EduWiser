import React, { useState } from 'react';
import { View, Swiper, SwiperItem, Image, Text } from '@tarojs/components';

const Home = () => {
  const [newsList, setNewsList] = useState([
    {
      id: 1,
      title: '最新资讯1',
      summary: '这是最新资讯1的摘要，点击查看更多详情。',
      image: '/assets/news1.jpg',
    },
    {
      id: 2,
      title: '最新资讯2',
      summary: '这是最新资讯2的摘要，点击查看更多详情。',
      image: '/assets/news2.jpg',
    },
    {
      id: 3,
      title: '最新资讯3',
      summary: '这是最新资讯3的摘要，点击查看更多详情。',
      image: '/assets/news3.jpg',
    },
  ]);

  return (
    <View className="home">
      {/* 轮播图 */}
      <Swiper className="home-swiper" indicatorDots autoplay interval={3000} circular>
        <SwiperItem>
          <Image className="swiper-image" src="/assets/slide1.jpg" />
        </SwiperItem>
        <SwiperItem>
          <Image className="swiper-image" src="/assets/slide2.jpg" />
        </SwiperItem>
        <SwiperItem>
          <Image className="swiper-image" src="/assets/slide3.jpg" />
        </SwiperItem>
      </Swiper>
      {/* 资讯框 */}
      <View className="news-section">
        <Text className="section-title">最新资讯</Text>
        {newsList.map(news => (
          <View key={news.id} className="news-item">
            <Image className="news-image" src={news.image} />
            <View className="news-content">
              <Text className="news-title">{news.title}</Text>
              <Text className="news-summary">{news.summary}</Text>
            </View>
          </View>
        ))}
      </View>
    </View>
  );
};

export default Home;
