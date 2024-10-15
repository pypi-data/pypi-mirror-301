import * as path from "path";
import * as vscode from "vscode";
import {
  collectPromptFiles,
  Node,
  PromptFileNode,
  PromptInputNode,
  TestSpecificationNode,
} from "./validation/discovery";
import { mergeNodeTree } from "./validation/session";

type RunnableNode = PromptFileNode | TestSpecificationNode | PromptInputNode;

let discoveredTests = new Map<string, RunnableNode>();

export function activate(context: vscode.ExtensionContext) {
  const testController = vscode.tests.createTestController(
    "promptarchitect.testController",
    "Prompt Architect"
  );

  testController.createRunProfile(
    "Run tests",
    vscode.TestRunProfileKind.Run,
    async (request) => {
      let nodes: RunnableNode[];

      if (request.include) {
        nodes = request.include.map((node) => {
          if (!discoveredTests.has(node.id)) {
            throw new Error(`Node ${node.id} not found in discovered tests`);
          }

          return discoveredTests.get(node.id)!;
        });
      } else {
        nodes = Array.from(discoveredTests.values());
      }

      console.log("Running tests", nodes);
    }
  );

  testController.refreshHandler = async () => {
    const nodeTree = await collectPromptFiles();
    mergeNodeTree(testController, nodeTree);
    cacheDiscoveredTests(nodeTree);
  };

  testController.resolveHandler = async (item) => {
    let nodeTree: Node[];

    if (item) {
      const workspaceFolder = vscode.workspace.workspaceFolders![0].uri.fsPath;
      const relativePath = path.relative(workspaceFolder, item.uri!.fsPath);

      nodeTree = await collectPromptFiles(relativePath);
    } else {
      nodeTree = await collectPromptFiles();
    }

    mergeNodeTree(testController, nodeTree);
    cacheDiscoveredTests(nodeTree);
  };

  context.subscriptions.push(testController);
}

function cacheDiscoveredTests(nodeTree: Node[], clearCache = true) {
  if (clearCache) {
    discoveredTests = new Map();
  }

  for (const node of nodeTree) {
    if (node.type !== "directory") {
      discoveredTests.set(node.id, node);
    }

    if (node.type !== "promptInput") {
      cacheDiscoveredTests(node.children, false);
    }
  }
}

export function deactivate() {}
