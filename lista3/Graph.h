#include <iostream>

class Edge {
public:
    int source;
    int destination;
    int cost;

    Edge(int source, int destination, int cost);
};

class Vertex {
public:
    int id;
    int numOfEdges;
    Edge** edges;

    Vertex(int id);
    ~Vertex();
    void addEdge(int destination, int cost);
};

class Data {
public:
    unsigned long long* d;
    long int time;

    Data(int vertices);
    ~Data();
};

class Element {
public:
    int id;
    unsigned long long cost;
    Element* next;

    Element(int id, unsigned long long cost);
};

class PriorityQueue {
public:
    Element* root;

    PriorityQueue();
    ~PriorityQueue();
    void insert(int id, unsigned long long cost);
    Element* pop();
    bool isEmpty();
};

class BucketElement {
public:
    int id;
    BucketElement* next;

    BucketElement(int id);
    ~BucketElement();
};

class Bucket {
public:
    BucketElement* root;

    Bucket();
    ~Bucket();
    void insert(int id);
    BucketElement* pop();
    bool isEmpty();
    int len();
};

class Graph {
public:
    int v;
    int e;
    int w;
    Vertex** vertices;

    Graph(int vertices, int edges);
    ~Graph();
    void addEdge(int source, int destination, int cost);
    Data* dijkstra(int source);
    Data* dial(int source);
    Data* radixHeap(int source);
};