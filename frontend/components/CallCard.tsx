import { Box, Heading, Text, Badge, Button, Stack } from '@chakra-ui/react';

interface Props {
  call: any;
  onFavorite?: (id: number) => void;
}

const CallCard = ({ call, onFavorite }: Props) => (
  <Box borderWidth="1px" borderRadius="lg" p={4} mb={4}>
    <Stack direction="row" justify="space-between" align="start">
      <Heading size="md">{call.title}</Heading>
      {call.deadline && <Badge colorScheme="red">Cierra: {call.deadline}</Badge>}
    </Stack>
    <Text fontSize="sm" color="gray.600">{call.organizer} · {call.country}</Text>
    <Text mt={2}>{call.description}</Text>
    <Stack direction="row" spacing={2} mt={2}>
      {call.tags?.map((tag: string) => (
        <Badge key={tag}>{tag}</Badge>
      ))}
    </Stack>
    <Stack direction="row" spacing={2} mt={4}>
      <Button as="a" href={call.source_url} target="_blank" rel="noopener noreferrer">Ver fuente</Button>
      {onFavorite && <Button onClick={() => onFavorite(call.id)}>Favorito</Button>}
    </Stack>
  </Box>
);

export default CallCard;
