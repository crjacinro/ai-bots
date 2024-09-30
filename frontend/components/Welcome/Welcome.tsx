import { Container, Title } from '@mantine/core';
import classes from './Welcome.module.css';
import ChatWindow from '../ChatWindow/ChatWindow';

export function Welcome() {
  return (
    <>
    <Container size="sm">
      <Title order={1} align="center" mt="xl" mb="xl">
        ChatGPT Clone
      </Title>
      <ChatWindow />
    </Container>
    </>
  );
}
