'use client';
'use strict';

import { Image, Carousel, Spin, Avatar } from 'antd';
import { LeftOutlined, RightOutlined, SendOutlined } from '@ant-design/icons';
import Search from "antd/es/input/Search";
import type { SearchProps } from 'antd/es/input/Search';
import { useState, useRef, useEffect } from "react";
import { UserInput } from "./components/user_input";

enum MessageType {
  Text,
  Swiper
}

export interface Message {
  type?: MessageType;
  title?: string;
  contents?: any;
}

export default function Home() {
  const [showAnimation, setShowAnimation] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const messageEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollTop = messageEndRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom(); // 页面渲染完成后执行滚动操作
  }, [messages]); // 依赖项为 messages

  useEffect(() => {
    if (messages.length > 0) {
      setShowAnimation(false);
    }
  }, [messages]);

  const onSearch: SearchProps['onSearch'] = async (value, _e, info) => {
    setMessages(messages => [...messages, {
      type: MessageType.Text,
      title: "You",
      contents: value,
    }]);

    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/api/dog_breed/?input=${value}`);
      const message: Message = {
        type: MessageType.Swiper,
        title: "Server",
        contents: null,
      };
      const responseData = await response.json();
      if (!response.ok) {
        console.error('Network response was not ok');
        message.type = MessageType.Text;
        message.contents = responseData["error"];
      }
      else {
        message.contents = responseData["data"];
      }

      setMessages(messages => [...messages, message]);
    } catch (error) {
      console.error('There was a problem fetching the data:', error);
    } finally {
      setLoading(false);
    }
    
    
    console.log(messages);
  }
  return (
    <main className="flex flex-col min-h-screen">
      <div className="flex-grow flex flex-col items-center justify-between p-24">
        {showAnimation && (
          <div className="text-4xl text-center animate-typing rainbow-text">Welcome to the page!</div>
        )}
        {showAnimation && (
          <div className="text-4xl text-center animate-typing rainbow-text">Input the number to see the dogs.</div>
        )}
        <div ref={messageEndRef} style={{ padding: '20px', width: '100%', minWidth: '400px', overflowY: 'auto', height:'800px' }}>
          {messages.map((message, index) => (
            <div key={index} style={{ marginBottom: '10px' }}>
              {
                message.type === MessageType.Text ? (<UserInput message={message}></UserInput>) : 
                (
                  <div>
                    <Avatar style={{ backgroundColor: '#33C8FF' }} icon={<SendOutlined />} /> Server:
                    <div className='justify-center'>
                      <Carousel autoplay arrows prevArrow={<LeftOutlined />} nextArrow={<RightOutlined />}>
                        {message.contents.map((image:string, idx:number) => (
                          <div key={idx} style={{ display: 'flex', justifyContent: 'center', height: '100%' }}>
                            <div style={{ backgroundColor: '#d6dbdc', height: '100%', display: 'flex', justifyContent: 'center' }}>
                              <Image
                                src={image}
                                style={{ height: '300px', width: '400px', objectFit: 'contain', margin: 'auto' }}
                                placeholder={
                                  <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                    <Spin size="large" />
                                  </div>
                                }
                              />
                            </div>
                          </div>
                        ))}
                      </Carousel>
                    </div>
                  </div>
                )
              }
            </div>
          ))}
        </div>
      </div>
      <div className="fixed bottom-0 left-0 w-full bg-white p-4">
        <div className="max-w-5xl mx-auto">
          <Search placeholder="input search text" loading={loading} enterButton="search" size="large" onSearch={onSearch} className="w-full" />
        </div>
      </div>
    </main>
  );
}