import { Title } from '@mantine/core';
import ChatWindow from '@/components/ChatWindow/ChatWindow';

export default function HomePage() {
  return (
    <>
        <Title order={1} align="center" mt="xl" mb="xl">
            Ai Bots Chat
        </Title>
      <ChatWindow />
    </>
  );
}
