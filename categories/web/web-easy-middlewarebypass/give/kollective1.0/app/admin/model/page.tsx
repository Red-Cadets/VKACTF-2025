'use client'
import { useState, useEffect } from 'react'
import { getCookie } from 'cookies-next'
import { getAllModels } from '@/app/actions/getModels'
import { addModel } from '@/app/actions/addModel' 
import { deleteModel } from '@/app/actions/deleteModel'
import { updateModel } from '@/app/actions/updateModel'

interface Robot {
  name: string
}

interface Model {
  id: number
  name: string
  robots: Robot[]
  combat: boolean
}

export default function ModelsPage() {
  const [models, setModels] = useState<Model[]>([])
  const [newModelName, setNewModelName] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isEditing, setIsEditing] = useState<number | null>(null)
  const [editedName, setEditedName] = useState<string>('')

  useEffect(() => {
    const fetchModels = async () => {
      try {
        setIsLoading(true)
        const models = await getAllModels()
        setModels(models)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Произошла ошибка')
      } finally {
        setIsLoading(false)
      }
    }

    fetchModels()
  }, [])

  const handleAddModel = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const newModel = await addModel(newModelName)  
      setModels([...models, newModel])
      setNewModelName('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      
      const response = await deleteModel(id)

      if (!response.ok) {
        throw new Error('Ошибка при удалении модели')
      }

      setModels(models.filter((model) => model.id !== id))
    } catch (error) {
      console.error(error)
    }
  }

  const handleEdit = (id: number, name: string) => {
    setIsEditing(id)
    setEditedName(name)
  }

  const handleSubmitEdit = async (id: number) => {
    try {
      if(id in [1,2,3,4]){
        throw new Error('Ошибка при обновлении модели')
      }else{
        const response = await updateModel(id, editedName)
        if (!response) {
          throw new Error('Ошибка при обновлении модели')
        }
  
        setModels(models.map((model) => (model.id === id ? { ...model, name: editedName } : model)))
  
        setIsEditing(null)
        setEditedName('')
      }
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="row g-4">
      <div className="col-lg-4">
        <div className="card shadow" style={{ backgroundColor: '#3a3a3a', borderColor: '#b0413e' }}>
          <div className="card-header text-white" style={{ backgroundColor: '#b0413e' }}>
            <h5 className="mb-0">Новая модель</h5>
          </div>
          <div className="card-body">
            {error && (
              <div className="alert alert-danger">
                <strong>Ошибка:</strong> {error}
              </div>
            )}
            <form onSubmit={handleAddModel}>
              <div className="mb-3">
                <label htmlFor="modelName" className="form-label text-white">Название модели</label>
                <input
                  type="text"
                  className="form-control text-white"
                  style={{ backgroundColor: '#2c2c2c', color: '#fff', borderColor: '#555' }}
                  id="modelName"
                  value={newModelName}
                  onChange={(e) => setNewModelName(e.target.value)}
                  placeholder="Введите название"
                  required
                />
              </div>
              <button type="submit" className="btn w-100 text-white" style={{ backgroundColor: '#b0413e' }} disabled={isLoading}>
                {isLoading ? 'Добавление...' : 'Добавить модель'}
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="col-lg-8">
        <div className="card shadow" style={{ backgroundColor: '#3a3a3a', borderColor: '#555' }}>
          <div className="card-header d-flex justify-content-between align-items-center" style={{ backgroundColor: '#444', color: '#fff' }}>
            <h5 className="mb-0">Зарегистрированные модели</h5>
            <span className="badge rounded-pill" style={{ backgroundColor: '#d1a75f', color: '#000' }}>
              {models.length} шт
            </span>
          </div>
          <div className="card-body">
            {isLoading && models.length === 0 ? (
              <div className="text-center">
                <div className="spinner-border text-warning" role="status"></div>
                <p className="mt-2">Загрузка данных...</p>
              </div>
            ) : models.length === 0 ? (
              <p className="text-center text-muted">Нет доступных моделей</p>
            ) : (
              <ul className="list-group list-group-flush">
                {models.map((model) => (
                  <li
                    key={model.id}
                    className="list-group-item"
                    style={{ backgroundColor: '#2c2c2c', color: '#e0e0e0', borderColor: '#444' }}
                  >
                    <div className="d-flex justify-content-between">
                      <div>
                        <h6 className="mb-1" style={{ color: model?.combat ? '#b0413e' : 'inherit' }}>{model.name} {model?.combat && (<i>Проект "Атомное Сердце"</i>)}</h6>
                        <div><small className="">ID: {model.id}</small></div>
                      </div>
                      <div className="d-flex gap-2">
                        {isEditing === model.id ? (
                          <>
                            <input
                              type="text"
                              className="form-control"
                              value={editedName}
                              onChange={(e) => setEditedName(e.target.value)}
                              placeholder="Новое название"
                            />
                            <button
                              className="btn btn-success btn-sm"
                              onClick={() => handleSubmitEdit(model.id)}
                            >
                              Отправить
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              className="btn btn-outline-light btn-sm"
                              onClick={() => handleEdit(model.id, model.name)}
                            >
                              Изменить
                            </button>
                            <button
                              className="btn btn-outline-danger btn-sm"
                              onClick={() => handleDelete(model.id)}
                            >
                              Удалить
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
