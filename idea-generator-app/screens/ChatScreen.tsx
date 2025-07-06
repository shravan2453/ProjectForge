import React, { useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  Keyboard,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import CustomHeader from '../screens/CustomHeader';
import { parseIdeaBlocks } from './IdeasScreen';

type Props = NativeStackScreenProps<RootStackParamList, 'Chat'>;

const BACKEND_URL = 'http://10.0.0.76:8000/lg-chat';   // adjust for device / network

/* ─── helper: render "**bold**" as actual bold text ─────────────────── */
const renderRichText = (content: string) => {
  // Match **bold** or *bold* and render as bold
  const parts = content.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  return parts.map((part, idx) => {
    if ((part.startsWith('**') && part.endsWith('**')) || (part.startsWith('*') && part.endsWith('*'))) {
      const txt = part.replace(/^\*+|\*+$/g, ''); // remove all leading/trailing asterisks
      return (
        <Text key={idx} style={{ fontWeight: 'bold' }}>
          {txt}
        </Text>
      );
    }
    return <Text key={idx}>{part}</Text>;
  });
};

export default function ChatScreen({ route, navigation }: Props) {
  const { previousMessages, preferences = [], formData, retainedIdeas, uploadedDocument } = route.params ?? {};
  const [messages, setMessages]   = useState(previousMessages ?? []);
  const [input, setInput]         = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [finalIdea, setFinalIdea] = useState<string | null>(null);
  const [threadId, setThreadId]   = useState<string | null>(null);
  const [isChecked, setIsChecked] = useState(false);
  const [isFinal, setIsFinal] = useState(false);
  const scrollRef = useRef<ScrollView>(null);
  const [inputFocused, setInputFocused] = useState(false);

  /* greet on first load */
  useEffect(() => {
    if ((!previousMessages || previousMessages.length === 0) && messages.length === 0) {
      setMessages([
        { role: 'assistant', content: 'Hello! Lets find a great project idea together.' }
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
      const requestData = {
        thread_id: threadId,
        messages: updated.slice(-8),
        preferences,
        uploaded_document: uploadedDocument ? {
          name: uploadedDocument.name,
          content: uploadedDocument.content
        } : null
      };

      const res = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
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
      setIsFinal(!!data.is_final);
    } catch (err) {
      console.error('❌ Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  /* ─── UI ──────────────────────────────────────────────────────────── */
  // Input bar style changes based on focus
  const inputBarPosition = inputFocused
    ? { position: 'absolute' as const, top: 445, left: 0, right: 0, zIndex: 20, borderTopWidth: 1, borderTopColor: '#e5e7eb',backgroundColor: 'white', padding: 5 }
    : { position: 'relative' as const, zIndex: 10, backgroundColor: 'white', borderTopWidth: 1, borderTopColor: '#e5e7eb', padding: 8 };
  const inputBarInnerStyle = inputFocused
    ? { minHeight: 48}
    : { minHeight: 48 };

  // Normal chat UI when keyboard is not visible
  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: 'white' }}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 80 : 0}
    >
      <SafeAreaView style={{ flex: 1, backgroundColor: 'white' }}>
        <View style={{ flexDirection: 'row', alignItems: 'center', height: 44 }}>
          {/* Left: Ideas */}
          <View style={{ minWidth: 80, alignItems: 'flex-start', paddingLeft: 16 }}>
            <TouchableOpacity
              onPress={() => {
                navigation.goBack();
              }}
            >
              <Text className="text-gray-600 text-base underline font-bold" style={{ fontFamily: 'Klados-Bold' }}>Ideas</Text>
            </TouchableOpacity>
          </View>
          {/* Center: Project Chat */}
          <View style={{ flex: 1, alignItems: 'center' }}>
            <Text className="text-black text-xl font-bold" style={{ fontFamily: 'Klados-Bold' }}>Project Chat</Text>
          </View>
          {/* Right: Log Out */}
          <View style={{ minWidth: 80, alignItems: 'flex-end', paddingRight: 16 }}>
            <TouchableOpacity
              onPress={() => {
                navigation.replace('HomeLogin');
              }}
            >
              <Text className="text-gray-600 text-base underline font-bold" style={{ fontFamily: 'Klados-Bold' }}>Log Out</Text>
            </TouchableOpacity>
          </View>
        </View>
        <ScrollView ref={scrollRef} className="flex-1 p-4"
          contentContainerStyle={{ paddingBottom: 3, paddingTop: 6 }}
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

          {finalIdea && isFinal && (
            <>
              <View className="p-4 bg-green-100 mt-4 rounded-xl">
                <Text className="text-lg font-bold mb-1">🎉 Final Project Idea</Text>
                <Text>{renderRichText(finalIdea)}</Text>
              </View>
              {/* Custom Checkbox and Submit button */}
              <TouchableOpacity
                style={{ flexDirection: 'row', alignItems: 'center', marginTop: 16 }}
                onPress={() => setIsChecked(!isChecked)}
                activeOpacity={0.7}
              >
                <View style={{
                  width: 24, height: 24, borderWidth: 2, borderColor: '#333', borderRadius: 6,
                  backgroundColor: isChecked ? '#333' : 'transparent', alignItems: 'center', justifyContent: 'center'
                }}>
                  {isChecked && <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold' }}>✓</Text>}
                </View>
                <Text style={{ marginLeft: 8, fontFamily: 'Klados-Bold', fontSize: 16 }}>I want to pick this idea.</Text>
              </TouchableOpacity>
              {isChecked && (
                <TouchableOpacity
                  style={{ marginTop: 16, backgroundColor: 'black', paddingVertical: 12, borderRadius: 8, alignItems: 'center' }}
                  onPress={() => {
                    // Parse finalIdea string into an object
                    const parsed = parseIdeaBlocks(finalIdea.split('\n'))[0];
                    navigation.navigate('Congrats', { selectedIdea: parsed });
                  }}
                >
                  <Text style={{ color: 'white', fontFamily: 'Klados-Bold', fontSize: 16 }}>Submit</Text>
                </TouchableOpacity>
              )}
            </>
          )}
        </ScrollView>
        {/* Input bar, now always visible, position and size change on focus */}
        {!finalIdea && (
          <View style={inputBarPosition}>
            <View className="flex-row items-center bg-white -mb-3" style={inputBarInnerStyle}>
              <TextInput
                value={input}
                onChangeText={setInput}
                placeholder="Type your message..."
                className="flex-1 bg-gray-100 p-2 rounded-xl mr-2 text-base"
                style={{ minHeight: 50, fontFamily: 'Klados-Bold' }}
                blurOnSubmit={false}
                onSubmitEditing={sendMessage}
                returnKeyType="send"
                onFocus={() => setInputFocused(true)}
                onBlur={() => setInputFocused(false)}
              />
              <TouchableOpacity
                className={`px-3.5 py-3.5 rounded-xl ${isLoading ? 'bg-gray-400' : 'bg-black'}`}
                onPress={sendMessage}
                disabled={isLoading}
              >
                <Text className="text-white font-bold" style={{ fontFamily: 'Klados-Bold'}}>Send</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </SafeAreaView>
    </KeyboardAvoidingView>
  );
}
