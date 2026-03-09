import React from 'react'
import { Camera } from 'lucide-react';
import { PromptBar } from './components/PromptBar';
import { ImageCanvas } from './components/ImageCanvas';
import { StatusDisplay } from './components/StatusDisplay';
import useImageGeneration from './hooks/useImageGeneration';

function App() {
    const { generateImage, status, result, error, loading } = useImageGeneration();

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col p-4 md:p-8">
            <div className="max-w-6xl w-full mx-auto space-y-8 flex-1 flex flex-col">
                {/* Header */}
                <div className="text-center space-y-4">
                    <div className="flex items-center justify-center space-x-3 mb-2">
                        <div className="p-3 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                            <Camera className="w-8 h-8 text-indigo-500" />
                        </div>
                        <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                            AI Vision Agent Pro
                        </h1>
                    </div>
                    <p className="text-slate-400 text-lg max-w-2xl mx-auto">
                        Professional-grade Agentic Image Generation Platform powered by SiliconFlow & LangGraph
                    </p>
                </div>

                {/* Main Content */}
                <div className="flex-1 flex flex-col items-center justify-center space-y-8">
                    <div className="w-full max-w-2xl min-h-[512px]">
                        <ImageCanvas image={result?.generated_image_url || result?.generated_image} loading={loading} />
                    </div>

                    <div className="w-full max-w-2xl space-y-4">
                        <PromptBar onGenerate={generateImage} loading={loading} />

                        <div className="flex justify-center min-h-[40px]">
                            <StatusDisplay status={status} error={error} />
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div className="text-center text-slate-600 text-sm py-4">
                    Powered by LangGraph • SiliconFlow • Langfuse
                </div>
            </div>
        </div>
    )
}

export default App
