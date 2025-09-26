import type { AppProps } from 'next/app';
import { ChakraProvider, Container, Box, Text } from '@chakra-ui/react';

const Disclaimer = () => (
  <Box bg="yellow.100" p={2} mb={4} borderRadius="md">
    <Text fontSize="sm">
      La información es agregada automáticamente y puede contener errores. Verifica siempre en la fuente antes de postular.
    </Text>
  </Box>
);

function ConvocaApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <Container maxW="6xl" py={6}>
        <Disclaimer />
        <Component {...pageProps} />
      </Container>
    </ChakraProvider>
  );
}

export default ConvocaApp;
