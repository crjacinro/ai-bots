import { Paper, Stack } from '@mantine/core';
import ChatMessage from '../ChatMessage/ChatMessage';
import ChatInput from '../ChatInput/ChatInput';
import { useState } from 'react';

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = (message) => {
    setMessages([...messages, { text: message, isUser: true }]);
    // Here you would typically call an API to get the AI response
  };

  return (
    <Paper shadow="xs" p="md">
      <Stack spacing="md">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg.text} isUser={msg.isUser} />
        ))}
      </Stack>
      <ChatInput onSendMessage={handleSendMessage} />
    </Paper>
  );
}