import { render, screen } from '@/test-utils';
import ChatWindow from './ChatWindow';

describe('Welcome component', () => {
  it('has correct Next.js theming section link', () => {
    render(<ChatWindow />);
    expect(screen.getByText('this guide')).toHaveAttribute(
      'href',
      'https://mantine.dev/guides/next/'
    );
  });
});
