import React, { useState, useRef } from 'react';
import { Upload, FileSpreadsheet, Play, AlertCircle, Loader2 } from 'lucide-react';

interface UploadSectionProps {
  onFileUpload: (file: File) => Promise<void>;
  onLoadDemo: () => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

export const UploadSection: React.FC<UploadSectionProps> = ({
  onFileUpload,
  onLoadDemo,
  isLoading,
  error,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      await onFileUpload(file);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      await onFileUpload(file);
      // reset input value so the same file can be re-selected if desired
      e.target.value = '';
    }
  };

  return (
    <div className="w-full mb-8">
      {/* Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isLoading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-6 md:p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-indigo-400 bg-indigo-950/30 scale-[1.005]'
            : 'border-slate-700 hover:border-slate-600 bg-slate-800/40 hover:bg-slate-800/60'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
          className="hidden"
          disabled={isLoading}
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            {isLoading ? (
              <Loader2 className="w-7 h-7 animate-spin text-indigo-400" />
            ) : (
              <FileSpreadsheet className="w-7 h-7" />
            )}
          </div>

          <div className="space-y-1">
            <h3 className="text-base font-semibold text-slate-100">
              {isLoading ? 'Processing and Analyzing Data...' : 'Drop your Google Sheet CSV or Excel export here'}
            </h3>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Supports <span className="text-slate-300 font-medium">.CSV</span> &amp; <span className="text-slate-300 font-medium">.XLSX</span> with columns:
              Timestamp, Date, Category, Description, Amount, Type
            </p>
          </div>

          {!isLoading && (
            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <button
                type="button"
                className="inline-flex items-center space-x-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded-lg shadow-sm transition-all shadow-indigo-600/30"
              >
                <Upload className="w-3.5 h-3.5" />
                <span>Select File</span>
              </button>

              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  onLoadDemo();
                }}
                className="inline-flex items-center space-x-1.5 px-4 py-2 bg-slate-700/80 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-medium rounded-lg border border-slate-600/80 transition-all shadow-sm"
              >
                <Play className="w-3.5 h-3.5 text-emerald-400 fill-emerald-400" />
                <span>Load SDP Demo Dataset</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="mt-4 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 flex items-start space-x-3 text-xs leading-relaxed">
          <AlertCircle className="w-4 h-4 text-rose-400 mt-0.5 flex-shrink-0" />
          <div className="flex-1">
            <strong className="font-semibold text-rose-200">Validation Notice: </strong>
            <span>{error}</span>
          </div>
        </div>
      )}
    </div>
  );
};

