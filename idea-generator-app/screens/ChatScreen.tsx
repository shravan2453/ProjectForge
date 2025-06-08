import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import CustomHeader from '../screens/CustomHeader';


type Props = NativeStackScreenProps<RootStackParamList, 'Chat'>;

export default function ChatScreen({ route, navigation }: Props) {
  const { previousMessages } = route.params;
  const [messages, setMessages] = useState(previousMessages ?? []);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [finalIdea, setFinalIdea] = useState<string | null>(null);

  useEffect(() => {
    if ((!previousMessages || previousMessages.length === 0) && messages.length === 0) {
      setMessages([
        { role: 'assistant', content: 'Hello! Let’s find a great project idea together.' }
      ]);
    }
  }, [previousMessages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const updatedMessages = [...messages, { role: 'user', content: input }];
    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/simple-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages.slice(-8) }) // limit history to last 8
      });

      const data = await response.json();
      if (data.assistant_message) {
        setMessages([...updatedMessages, { role: 'assistant', content: data.assistant_message }]);
        if (data.final_idea) {
          setFinalIdea(data.final_idea);
        }
      }
    } catch (err) {
      console.error('❌ Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView className="flex-1 bg-white" behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View className="mt-6">
        <CustomHeader title="Project Chat" />
      </View>

      <ScrollView className="mb-0 flex-1 p-4" contentContainerStyle={{ paddingBottom: 160, paddingTop: 24 }}>
        {messages.map((msg, index) => (
          <View
            key={index}
            className={`mb-4 p-3 rounded-xl ${msg.role === 'user' ? 'bg-blue-100 self-end' : 'bg-gray-100 self-start'}`}
            style={{ maxWidth: '80%' }}
          >
            <Text className="text-sm text-black">{msg.content}</Text>
          </View>
        ))}

        {finalIdea && (
          <View className="p-4 bg-green-100 mt-4 rounded-xl">
            <Text className="text-lg font-bold mb-1">🎉 Final Project Idea</Text>
            <Text>{finalIdea}</Text>
          </View>
        )}
      </ScrollView>

      {!finalIdea && (
        <View style={{ position: 'absolute', left: 0, right: 0, bottom: 0, padding: 16, backgroundColor: 'white' }}>
          <View className="flex-row items-center border-t border-gray-200 bg-white" style={{ minHeight: 64 }}>
            <TextInput
              value={input}
              onChangeText={setInput}
              placeholder="Type your message..."
              className="flex-1 bg-gray-100 p-4 rounded-xl mr-2 text-base"
              style={{ minHeight: 40 }}
            />
            <TouchableOpacity
              className={`px-4 py-2 rounded-xl ${isLoading ? 'bg-gray-400' : 'bg-black'}`}
              onPress={sendMessage}
              disabled={isLoading}
            >
              <Text className="text-white font-bold">Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </KeyboardAvoidingView>
  );
}
