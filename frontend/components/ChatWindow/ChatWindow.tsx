import { useEffect, useState } from 'react';
import {Container, TextInput, Button, Box, Text} from '@mantine/core';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

type Message = {
  id: number;
  content: string;
  sender: 'user' | 'bot';
};



export default function ChatWindow() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const queryClient = useQueryClient();
  const [conversationId, setConversationId] = useState('')

  useEffect(() => {
    fetch('http://localhost:8000/conversations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: "New Conversation",
        llm_params: {
            model_name: "gpt-3.5-turbo",
            temperature: 0.25
        }
      }),
    })
    .then(r => r.json())
    .then(r => {
      setConversationId(r.id)
   }).catch(error => console.error('Error', error))
  }, []);

  const sendMessageToServer = async (message: string) => {
    const response = await fetch('http://localhost:8000/queries/'+conversationId, {
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

  const mutation = useMutation({
      mutationFn: sendMessageToServer,
      onSuccess: (data, variables) => {
          const botMessage = { id: Date.now(), content: data.response, sender: 'bot' };
          setMessages((prev) => [...prev, botMessage]);
      },
  });

  const handleSend = () => {
      if (input.trim()) {
          const userMessage = { id: Date.now(), content: input, sender: 'user' };
          setMessages((prev) => [...prev, userMessage]);
          mutation.mutate(input);
          setInput('');
      }
  };

  return (
      <Container>
        <Box mb="md">
          {messages.map((msg) => (
            <Box>
              <Box bg={msg.sender === 'user' ? 'blue' : 'green'} m={16} p={16} style={{ '--radius': '0.5rem', borderRadius: 'var(--radius)', width: 'auto', display: 'inline-block'}} >
                <Text key={msg.id} align={msg.sender === 'user' ? 'right' : 'left'} >
                  {msg.sender}: {msg.content}
                </Text>
              </Box>
            </Box>
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
