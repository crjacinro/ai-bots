import { useState } from 'react';
import {Container, TextInput, Button, Box, Text} from '@mantine/core';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

type Message = {
  id: number;
  content: string;
  sender: 'user' | 'bot';
};

const fakeApiCall = async (message: string) => {
    const response = await fetch('http://localhost:8000/queries/66f96a1e5febabc559dbf602', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            role: 'user',
            content: message,
        }),
    });
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
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

    // useMutation to simulate sending the user's message to the fake API
    const mutation = useMutation({
        mutationFn: fakeApiCall,
        onSuccess: (data, variables) => {
            const botMessage = { id: Date.now(), content: data.response, sender: 'bot' };
            setMessages((prev) => [...prev, botMessage]); // Append the bot response to the messages
        },
    });

    const handleSend = () => {
        if (input.trim()) {
            const userMessage = { id: Date.now(), content: input, sender: 'user' };
            setMessages((prev) => [...prev, userMessage]); // Add user's message to the chat
            mutation.mutate(input); // Call the fake API with user's input
            setInput(''); // Clear input field
        }
    };

  const handleSendOld = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
      <Container>
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
