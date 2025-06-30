import React, { useEffect, useRef, useState } from 'react';
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

const BACKEND_URL = 'http://127.0.0.1:8000/lg-chat';   // adjust for device / network

/* ─── helper: render "**bold**" as actual bold text ─────────────────── */
const renderRichText = (content: string) => {
  // split on **…**
  const parts = content.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, idx) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      const txt = part.slice(2, -2);                // remove the asterisks
      return (
        <Text key={idx} style={{ fontWeight: 'bold' }}>
          {txt}
        </Text>
      );
    }
    return <Text key={idx}>{part}</Text>;
  });
};

export default function ChatScreen({ route }: Props) {
  const { previousMessages, preferences = [] } = route.params ?? {};
  const [messages, setMessages]   = useState(previousMessages ?? []);
  const [input, setInput]         = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [finalIdea, setFinalIdea] = useState<string | null>(null);
  const [threadId, setThreadId]   = useState<string | null>(null);
  const scrollRef = useRef<ScrollView>(null);

  /* greet on first load */
  useEffect(() => {
    if ((!previousMessages || previousMessages.length === 0) && messages.length === 0) {
      setMessages([
        { role: 'assistant', content: 'Hello! Let’s find a great project idea together.' }
      ]);
    }
  }, []);

  /* ─── send message to backend ─────────────────────────────────────── */
  const sendMessage = async () => {
    if (!input.trim()) return;
    const updated = [...messages, { role: 'user', content: input }];
    setMessages(updated);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          thread_id      : threadId,
          messages       : updated.slice(-8),
          preferences
        })
      });
      const data = await res.json();
      if (!threadId && data.thread_id) setThreadId(data.thread_id);

      if (data.assistant_message) {
        setMessages([
          ...updated,
          { role: 'assistant', content: data.assistant_message }
        ]);
      }
      if (data.final_idea) setFinalIdea(data.final_idea);
    } catch (err) {
      console.error('❌ Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  /* ─── UI ──────────────────────────────────────────────────────────── */
  return (
    <KeyboardAvoidingView className="flex-1 bg-white"
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View className="mt-6">
        <CustomHeader title="Project Chat" />
      </View>

      <ScrollView ref={scrollRef} className="flex-1 p-4"
        contentContainerStyle={{ paddingBottom: 160, paddingTop: 24 }}
        onContentSizeChange={() =>             
          scrollRef.current?.scrollToEnd({ animated: true })
        }>
        {messages.map((msg, idx) => (
          <View
            key={idx}
            className={`mb-4 p-3 rounded-xl ${
              msg.role === 'user' ? 'bg-blue-100 self-end' : 'bg-gray-100 self-start'
            }`}
            style={{ maxWidth: '80%' }}
          >
            {/* replace plain text with rich renderer */}
            <Text className="text-sm text-black">{renderRichText(msg.content)}</Text>
          </View>
        ))}

        {finalIdea && (
          <View className="p-4 bg-green-100 mt-4 rounded-xl">
            <Text className="text-lg font-bold mb-1">🎉 Final Project Idea</Text>
            <Text>{renderRichText(finalIdea)}</Text>
          </View>
        )}
      </ScrollView>

      {!finalIdea && (
        <View style={{
          position: 'absolute', left: 0, right: 0, bottom: 5,
          padding: 16, backgroundColor: 'white'
        }}>
          <View className="flex-row items-center border-t border-gray-200 bg-white"
            style={{ minHeight: 64 }}>
            <TextInput
              value={input}
              onChangeText={setInput}
              placeholder="Type your message..."
              className="flex-1 bg-gray-100 p-4 rounded-xl mr-2 text-base"
              style={{ minHeight: 40, fontFamily: 'Klados-Bold' }}
            />
            <TouchableOpacity
              className={`px-4 py-2 rounded-xl ${isLoading ? 'bg-gray-400' : 'bg-black'}`}
              onPress={sendMessage}
              disabled={isLoading}
            >
              <Text className="text-white font-bold" style={{ fontFamily: 'Klados-Bold'}}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </KeyboardAvoidingView>
  );
}
