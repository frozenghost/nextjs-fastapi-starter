'use client';
'use strict';

import Image from "next/image";
import Link from "next/link";
import { InputNumber, Carousel } from 'antd';
import Search from "antd/es/input/Search";
import type { SearchProps } from 'antd/es/input/Search';
import { useState } from "react";

export enum MessageType {
  Text,
  Swiper
}

type MessageKeys = keyof typeof MessageType;

class Message {
  type?: MessageType;
  contents?: any;
}

export default function Home() {
  const [messages, setMessages] = useState(Array<Message>());
  const onSearch: SearchProps['onSearch'] = (value, _e, info) => {
    setMessages([...messages, {
      type: MessageType.Text,
      contents: value,
    }]);
    console.log(messages);
  }
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
          123123213
        </div>
      </div>

      <div style={{ padding: '20px' }}>
            <div style={{ marginBottom: '20px' }}>
              {messages.map((message, index) => (
                <div key={index} style={{ marginBottom: '10px' }}>
                  <p>User: {message.contents}</p>
                  {/* <Carousel autoplay>
                    {message.contents.map((image, idx) => (
                      <div key={idx}>
                        <img src={image} alt={`Dog ${idx + 1}`} style={{ width: '100%' }} />
                      </div>
                    ))}
                  </Carousel> */}
                </div>
              ))}
            </div>
          </div>

      <div className="mb-32 grid text-center lg:mb-0 w-full lg:text-left">
        <Search placeholder="input search text" enterButton="search" size="large" onSearch={onSearch} />
      </div>
    </main>
  );
}
