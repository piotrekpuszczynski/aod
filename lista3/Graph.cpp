#include <limits>
#include <sys/time.h>
#include "Graph.h"

/** edge methods */
Edge::Edge(int source, int destination, int cost) {
    this->source = source;
    this->destination = destination;
    this->cost = cost;
}

/** vertex methods */
Vertex::Vertex(int id) {
    this->id = id;
    this->numOfEdges = 0;
}

void Vertex::addEdge(int destination, int cost) {
    this->numOfEdges++;
    Edge** temp = new Edge*[this->numOfEdges];
    for (int i = 0; i < this->numOfEdges - 1; i++) {
        temp[i] = this->edges[i];
    }
    temp[numOfEdges - 1] = new Edge(this->id, destination, cost);
    this->edges = temp;
}

Vertex::~Vertex() {
    delete []edges;
};

/** data methods */
Data::Data(int vertices) {
    this->d = new unsigned long long[vertices];

    for (int i = 0; i < vertices; i++) {
        d[i] = std::numeric_limits<unsigned long long>::max();
    }
};

Data::~Data() {
    delete []d;
}

/** element methods */
Element::Element(int id, unsigned long long cost) {
    this->id = id;
    this->cost = cost;
    this->next = nullptr;
}

/** priority queue methods */
PriorityQueue::PriorityQueue() {
    this->root = nullptr;
}

void PriorityQueue::insert(int id, unsigned long long cost) {
    Element* element = new Element(id, cost);

    if (isEmpty() || cost < this->root->cost) {
        element->next = this->root;
        this->root = element;
    } else {
        Element* temp = this->root;
        while (temp->next != nullptr && temp->next->cost <= cost) {
            temp = temp->next;
        }

        element->next = temp->next;
        temp->next = element;
    }
}

Element* PriorityQueue::pop() {
    if (!isEmpty()) {
        Element* temp = this->root;
        this->root = this->root->next;
        return temp;
    }
    return nullptr;

}

bool PriorityQueue::isEmpty() {
    return this->root == nullptr;
}

PriorityQueue::~PriorityQueue() {
    while (!isEmpty()) {
        Element* temp = pop();
        delete temp;
    }
}

/** bucket element methods */
BucketElement::BucketElement(int id) {
    this->id = id;
    this->next = nullptr;
}

BucketElement::~BucketElement() {
    delete next;
}

/** bucket methods */
Bucket::Bucket() {
    this->root = nullptr;
}

void Bucket::insert(int id) {
    BucketElement* temp = new BucketElement(id);
    temp->next = this->root;
    this->root = temp;
}

BucketElement* Bucket::pop() {
    if (!isEmpty()) {
        BucketElement* temp = this->root;
        this->root = this->root->next;
        return temp;
    }
    return nullptr;
}

bool Bucket::isEmpty() {
    return this->root == nullptr;
}

int Bucket::len() {
    int i = 0;
    BucketElement* cur = this->root;
    while (cur != nullptr) {
        cur = cur->next;
        i++;
    }
    return i;
}

Bucket::~Bucket() {
    while (!isEmpty()) {
        delete pop();
    }
}

/** graph methods */
void Graph::addEdge(int source, int destination, int cost) {
    if (this->w < cost) this->w = cost;
    this->vertices[source - 1]->addEdge(destination - 1, cost);
}

Data* Graph::dijkstra(int source) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    long int start = tp.tv_sec * 1000 + tp.tv_usec / 1000;

    Data* data = new Data(this->v);
    PriorityQueue* Q = new PriorityQueue();
    data->d[source] = 0;
    Q->insert(source, data->d[source]);

    while (!Q->isEmpty()) {
        Element* cur = Q->pop();
        Vertex* v = this->vertices[cur->id];
        free(cur);
        for (int i = 0; i < v->numOfEdges; i++) {
            Edge* edge = v->edges[i];
            if (data->d[edge->destination] > data->d[edge->source] + edge->cost) {
                data->d[edge->destination] = data->d[edge->source] + edge->cost;
                Q->insert(edge->destination, data->d[edge->destination]);
            }
        }
    }

    gettimeofday(&tp, NULL);
    long int stop = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    data->time = stop - start;

    return data;
}

Data* Graph::dial(int source) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    long int start = tp.tv_sec * 1000 + tp.tv_usec / 1000;

    Data* data = new Data(this->v);
    unsigned long long w = this->w;
    w = w * this->v + 1;
    Bucket** B = new Bucket*[w];
    for (unsigned long long i = 0; i < w; i++) B[i] = new Bucket();

    data->d[source] = 0;
    B[0]->insert(source);
    for (unsigned long long i = 0; i < w; i++) {
        while (!B[i]->isEmpty()) {
            BucketElement* cur = B[i]->pop();
            if (data->d[cur->id] < i) continue;
            Vertex* v = this->vertices[cur->id];
            for (int i = 0; i < v->numOfEdges; i++) {
                Edge* edge = v->edges[i];
                if (data->d[edge->destination] > data->d[edge->source] + edge->cost) {
                    data->d[edge->destination] = data->d[edge->source] + edge->cost;
                    B[data->d[edge->destination]]->insert(edge->destination);
                }
            }
        }
    }

    gettimeofday(&tp, NULL);
    long int stop = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    data->time = stop - start;

    return data;
}

int getBucketIndex(int id) {
    int len = 0;
    int pow = 1;
    int sum = 0;
    while (sum < id) {
        sum += pow;
        pow *= 2;
        len++;
    }
    return len;
}

Data* Graph::radixHeap(int source) {
    struct timeval tp;
    gettimeofday(&tp, NULL);
    long int start = tp.tv_sec * 1000 + tp.tv_usec / 1000;

    Data* data = new Data(this->v);
    unsigned long long w = this->w;
    w = w * this->v;
    w = getBucketIndex(w) + 1;
    Bucket** B = new Bucket*[w];
    for (int i = 0; i < w; i++) B[i] = new Bucket();

    data->d[source] = 0;
    B[0]->insert(source);

    for (int i = 0; i < w; i++) {
        int len = B[i]->len();
        if (len == 1 || i == 0 || i == 1) {
            while (!B[i]->isEmpty()) {
                BucketElement* cur = B[i]->pop();
                Vertex* v = this->vertices[cur->id];
                for (int i = 0; i < v->numOfEdges; i++) {
                    Edge* edge = v->edges[i];
                    if (data->d[edge->destination] > data->d[edge->source] + edge->cost) {
                        data->d[edge->destination] = data->d[edge->source] + edge->cost;
                        B[getBucketIndex(data->d[edge->destination])]->insert(edge->destination);
                    }
                }
                if (B[i]->len() >= 1 && i != 0 && i != 1) {
                    i--;
                    break;
                }
            }
        } else if (len > 1) {
            int* vertices = new int[len];
            BucketElement* cur = B[i]->pop();
            vertices[0] = cur->id;
            int min = data->d[cur->id];
            int counter = 1;
            while (!B[i]->isEmpty()) {
                cur = B[i]->pop();
                vertices[counter] = cur->id;
                if (min > data->d[cur->id]) {
                    min = data->d[cur->id];
                }
                counter++;
            }
            for (int j = 0; j < len; j++) {
                B[getBucketIndex(data->d[vertices[j]] - min)]->insert(vertices[j]);
            }
            free(vertices);
            i = -1;
        }
    }
    free(B);

    gettimeofday(&tp, NULL);
    long int stop = tp.tv_sec * 1000 + tp.tv_usec / 1000;
    data->time = stop - start;

    return data;
}

Graph::Graph(int vertices, int edges) {
    this->v = vertices;
    this->e = edges;
    this->w = 0;
    this->vertices = new Vertex*[vertices];
    for (int i = 0; i < vertices; i++) {
        this->vertices[i] = new Vertex(i);
    }
}

Graph::~Graph() {
    delete []vertices;
};
