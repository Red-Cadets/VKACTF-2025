'use client';

import { useState } from 'react';
import { processFile } from '@/app/actions/loadDump';

export default function DumpPage() {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] ?? null;

    if (selectedFile) {
      const fileExtension = selectedFile.name.split('.').pop()?.toLowerCase();
      if (fileExtension === 'sql') {
        setFile(selectedFile);
        setError('');
      } else {
        setFile(null);
        setError('Пожалуйста, выберите файл с расширением .sql');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      setError('Файл не выбран');
      return;
    }

    setIsLoading(true);
    setError('');
    setMessage('');

    try {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const text = e.target?.result?.toString() ?? '';

        try {
          const result = await processFile(text); 
          setMessage(result.status);
        } catch (err: any) {
          setError('Ошибка при обработке дампа: ' + err.message);
        } finally {
          setIsLoading(false);
        }
      };
      reader.readAsText(file);
    } catch (err: any) {
      setError('Ошибка при чтении файла');
      setIsLoading(false);
    }
  };

  return (
    <div className="row g-4">
      <div className="col-lg-6">
        <div className="card shadow" style={{ backgroundColor: '#3a3a3a', borderColor: '#b0413e' }}>
          <div className="card-header text-white" style={{ backgroundColor: '#b0413e' }}>
            <h5 className="mb-0">Загрузка SQL дампа</h5>
          </div>
          <div className="card-body">
            {error && (
              <div className="alert alert-danger">
                <strong>Ошибка:</strong> {error}
              </div>
            )}
            {message && (
              <div className="alert alert-success">
                <strong>Успех:</strong> {message}
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="file" className="form-label text-white">Выберите файл .sql</label>
                <input
                  type="file"
                  className="form-control"
                  id="file"
                  accept=".sql"
                  onChange={handleFileChange}
                  required
                />
              </div>
              <button type="submit" className="btn w-100 text-white" style={{ backgroundColor: '#b0413e' }} disabled={isLoading}>
                {isLoading ? 'Загрузка...' : 'Загрузить дамп'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
