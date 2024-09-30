import { Text, Box } from '@mantine/core';

export default function ChatMessage({ message, isUser }) {
  return (
    <Box bg={isUser ? 'blue.1' : 'gray.1'} p="xs" style={{ borderRadius: '8px' }}>
      <Text>{message}</Text>
    </Box>
  );
}