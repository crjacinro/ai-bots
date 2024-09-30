import { useState } from 'react';
import {Container, TextInput, Button, Box, Text, Title} from '@mantine/core';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

type Message = {
  id: number;
  content: string;
  sender: 'user' | 'bot';
};
export default function Welcome() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const queryClient = useQueryClient();

  const sendMessage = (message: string) => {
    const userMessage = { id: Date.now(), content: message, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);

    // Simulate bot response
    setTimeout(() => {
      const botMessage = { id: Date.now(), content: `Bot response to "${message}"`, sender: 'bot' };
      setMessages((prev) => [...prev, botMessage]);
    }, 1000);
  };

  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
      <Container>
          <Title order={1} align="center" mt="xl" mb="xl">
              ChatGPT Clone
          </Title>
        <Box mb="md">
          {messages.map((msg) => (
              <Text key={msg.id} align={msg.sender === 'user' ? 'right' : 'left'}>
                {msg.sender}: {msg.content}
              </Text>
          ))}
        </Box>
        <TextInput
            placeholder="Type your message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
        />
        <Button mt="sm" onClick={handleSend}>
          Send
        </Button>
      </Container>
  );
}
