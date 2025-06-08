'use client'

import { addOrder } from "@/app/actions/addOrder";
import { getAllOrders } from "@/app/actions/getAllOrders";
import { getAllModels } from "@/app/actions/getModels";
import { useEffect, useState } from "react";
import { Form, Button, Card } from "react-bootstrap";

interface Model {
  id: number;
  name: string;
}

interface Order {
  id: number;
  message: string;
  modelId: number;
  model: Model;
}

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [models, setModels] = useState<Model[]>([]);
  const [message, setMessage] = useState("");
  const [selectedModel, setSelectedModel] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchOrders();
    fetchModels();
  }, []);

  const fetchOrders = async () => {
    const res = await getAllOrders();
    setOrders(res);
  };

  const fetchModels = async () => {
    const res = await getAllModels();
    setModels(res);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message || !selectedModel) return;
    setLoading(true);
    try {
      const response = await addOrder(message, selectedModel)
      setMessage("");
      setSelectedModel(null);
      fetchOrders();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-4" style={{ fontFamily: "'Orbitron', sans-serif", color: "#d1a75f" }}>
        Приказы
      </h2>

      <Form onSubmit={handleSubmit} className="mb-5">
        <Form.Group className="mb-3">
          <Form.Label className="text-light">Сообщение приказа</Form.Label>
          <Form.Control
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Введите приказ"
            style={{ backgroundColor: "#333", borderColor: "#444", color: "#fff" }}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label className="text-light">Выберите модель</Form.Label>
          <Form.Select
            value={selectedModel || ""}
            onChange={(e) => setSelectedModel(Number(e.target.value))}
            style={{ backgroundColor: "#333", borderColor: "#444", color: "#fff" }}
          >
            <option value="" disabled>Выберите модель</option>
            {models.map((model) => (
              <option key={model.id} value={model.id}>{model.name}</option>
            ))}
          </Form.Select>
        </Form.Group>

        <Button
          variant="danger"
          type="submit"
          disabled={loading}
          style={{ backgroundColor: "#d1a75f", borderColor: "#d1a75f" }}
        >
          {loading ? "Отправка..." : "Отправить приказ"}
        </Button>
      </Form>

      <div className="d-flex flex-wrap gap-3">
        {orders.map((order) => (
          <Card
            key={order.id}
            style={{
              width: "18rem",
              backgroundColor: "#1e1e1e",
              borderColor: "#d1a75f",
              borderRadius: "10px",
            }}
            text="light"
          >
            <Card.Body>
              <Card.Title style={{ color: "#d1a75f" }}>{order.model.name}</Card.Title>
              <Card.Text>{order.message}</Card.Text>
            </Card.Body>
          </Card>
        ))}
      </div>
    </div>
  );
}
