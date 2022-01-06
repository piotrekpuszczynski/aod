#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include "Graph.h"

using namespace std;

string getWoComment(string path) {
    string result = "";

    ifstream File(path);
    string text;
    while (getline(File, text)) {
        if (text.substr(0, 1) == "c") continue;
        result.append(text);
        result.append("\n");
    }
    File.close();

    return result;
}

string getLine(string* str) {
    size_t pos = 0;
    string token;
    if ((pos = str->find("\n")) != string::npos) {
        token = str->substr(0, pos);
        str->erase(0, pos + 1);
        return token + " ";
    }
    return "";
}

string getIndex(string str, int index) {
    size_t pos = 0;
    string token;
    for (int i = 0; i < index; i++) {
        if ((pos = str.find(" ")) == string::npos) return "";
        token = str.substr(0, pos);
        str.erase(0, pos + 1);
    }
    return token;
}

Graph* load(string path) {
    string woComment = getWoComment(path);

    Graph* graph;
    string line = getLine(&woComment);
    int edges = stoi(getIndex(line, 4));
    graph = new Graph(stoi(getIndex(line, 3)), edges);
    for (int i = 0; i < edges; i++) {
        line = getLine(&woComment);
        int source = stoi(getIndex(line, 2));
        int destination = stoi(getIndex(line, 3));
        int cost = stoi(getIndex(line, 4));
        graph->addEdge(source, destination, cost);
    }

    return graph;
}

string* getParameters(int argc, char** argv) {
    if (argc != 8) return nullptr;
    string* temp = new string[8];
    for (int i = 0; i < 8; i++) {
        temp[i] += argv[i];
    }

    string* params = new string[5];
    params[0] = temp[1];
    for (int i = 2; i < 8; i += 2) {
        if (!temp[i].compare("-d")) {
            params[2] = temp[i + 1];
        } else if ((!temp[i].compare("-ss")) || (!temp[i].compare("-p2p"))) {
            params[3] = temp[i + 1];
        } else if ((!temp[i].compare("-oss")) || (!temp[i].compare("-op2p"))) {
            params[4] = temp[i + 1];
        } else {
            return nullptr;
        }
    }
    if (params[2].substr(params[2].size() - 3, params[2].size()).compare(".gr")) {
        return nullptr;
    }
    if (!params[3].substr(params[3].size() - 3, params[3].size()).compare(".ss") &&
            !params[4].substr(params[4].size() - 7, params[4].size()).compare(".ss.res")) {
        params[1] = "ss";
    } else if (!params[3].substr(params[3].size() - 4, params[3].size()).compare(".p2p") &&
                !params[4].substr(params[4].size() - 8, params[4].size()).compare(".p2p.res")) {
        params[1] = "p2p";
    } else {
        return nullptr;
    }
    return params;
}

Data* getData(Graph* graph, string algorithm, int source) {
    if (!algorithm.compare("dijkstra")) {
        return graph->dijkstra(source);
    } else if (!algorithm.compare("dial")) {
        return graph->dial(source);
    } else if (!algorithm.compare("radixheap")) {
        return graph->radixHeap(source);
    } else {
        return nullptr;
    }
}

int* getSources(string type, string path) {
    string woComment = getWoComment(path);
    string line = getLine(&woComment);
    int* s;
    int sources = stoi(getIndex(line, 5));
    if (!type.compare("ss")) {
        if (getIndex(line, 4).compare("ss")) return nullptr;
        s = new int[sources + 1];
    } else if (!type.compare("p2p")) {
        if (getIndex(line, 4).compare("p2p")) return nullptr;
        s = new int[sources * 2 + 1];
    }

    s[0] = sources;
    for (int i = 0; i < sources; i++) {
        line = getLine(&woComment);
        if (!type.compare("ss")) {
            s[i + 1] = stoi(getIndex(line, 2));
        } else {
            s[2 * i + 1] = stoi(getIndex(line, 2));
            s[2 * i + 2] = stoi(getIndex(line, 3));
        }
    }

    return s;
}

void createResultFile(string* params, Graph* graph, int* sources) {
    ofstream file("out/" + params[4]);

    file << "p res sp ";
    file << params[1] + " ";
    file << params[0] + "\n";

    file << "f ";
    file << params[2] + " ";
    file << params[3] + "\n";

    file << "g ";
    file << graph->v;
    file << " ";
    file << graph->e;
    file << " 0 ";
    file << graph->w;
    file << "\n";

    if (!params[1].compare("ss")) {
        float avr = 0;
        for (int i = 1; i < sources[0] + 1; i++) {
            Data* data = getData(graph, params[0], sources[i] - 1);
            avr += data->time;
        }
        avr /= sources[0];
        file << "t ";
        file << avr;
        file << "\n";

    } else {
        for (int i = 1; i < sources[0] * 2 + 1; i += 2) {
            Data* data = getData(graph, params[0], sources[i] - 1);
            file << "d ";
            file << sources[i];
            file << " ";
            file << sources[i + 1];
            file << " ";
            file << data->d[sources[i + 1] - 1];
            file << "\n";
        }
    }

    file.close();
}

string getAvr(string algorithm, int i) {
    int* sources = getSources("ss", "in/Random4-n." + to_string(i) + ".0.ss");
    Graph* graph = load("in/Random4-n." + to_string(i) + ".0.gr");
    float avr = 0;
    for (int j = 1; j < sources[0] + 1; j++) {
        Data* data = getData(graph, algorithm, sources[j] - 1);
        avr += data->time;
    }
    avr /= sources[0];
    return to_string(avr) + "\n";
}

void test() {
    ofstream dijkstra("tests/dijkstra");
    ofstream dial("tests/dial");
    ofstream radix("tests/radix");

    for (int i = 10; i < 15; i++) {
        dijkstra << getAvr("dijkstra", i);
//        dial << getAvr("dial", i);
        radix << getAvr("radixheap", i);
    }

    dijkstra.close();
    dial.close();
    radix.close();
}

int main(int argc, char **argv) {
    string* params = getParameters(argc, argv);
    if (params == nullptr) return -1;
    int* sources = getSources(params[1], "in/" + params[3]);
    if (sources == nullptr) return -2;
    Graph* graph = load("in/" + params[2]);
//    Data* d = graph->dial(0);
//    for (int i = 0; i < graph->v; i++) cout<<d->d[i]<<endl;
    createResultFile(params, graph, sources);
//    test();
    return 0;
}
