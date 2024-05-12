import { Avatar } from "antd";
import { UserOutlined, SendOutlined } from '@ant-design/icons';
import { Message } from "../page";

export const UserInput = ({ message }: { message: Message }) => {
    return (
        <div className="grid grid-cols-9 gap-4">
            <div className="col-span-1">
                {message.title === "You" ? (<Avatar style={{ backgroundColor: '#87d068' }} icon={ <UserOutlined />} />) :
                    (<Avatar style={{ backgroundColor: '#33C8FF' }} icon={ <SendOutlined /> } />)
                }
                <span>
                    &nbsp;{message.title}:
                </span>
            </div>
            <div className="col-span-8 align-middle text-xl">{message.contents}</div>
        </div>
    );
}