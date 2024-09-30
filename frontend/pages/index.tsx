import { Title } from '@mantine/core';
import Welcome from '@/components/Welcome/Welcome';

export default function HomePage() {
  return (
    <>
        <Title order={1} align="center" mt="xl" mb="xl">
            Ai Bots Chat
        </Title>
      <Welcome />
    </>
  );
}
