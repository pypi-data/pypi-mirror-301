import * as path from "path";
import * as vscode from "vscode";
import { Node } from "./discovery";

export function mergeNodeTree(
  controller: vscode.TestController,
  nodes: Node[]
) {
  const workspacePath = vscode.workspace.workspaceFolders![0].uri.fsPath;

  function mergeNodes(parent: vscode.TestItem, node: Node) {
    if (node.type === "promptInput") {
      return;
    }

    for (const childItem of node.children) {
      let childTestItem = parent.children.get(childItem.name);

      if (!childTestItem) {
        childTestItem = controller.createTestItem(
          childItem.id,
          childItem.name,
          vscode.Uri.file(path.join(workspacePath, childItem.path))
        );

        parent.children.add(childTestItem);
      }

      parent.children.forEach((child) => {
        if (!node.children.some((n) => n.id === child.id)) {
          parent.children.delete(child.id);
        }
      });

      mergeNodes(childTestItem, childItem);
    }
  }

  for (const node of nodes) {
    let testItem = controller.items.get(node.path);

    if (!testItem) {
      testItem = controller.createTestItem(
        node.id,
        node.name,
        vscode.Uri.file(path.join(workspacePath, node.path))
      );

      controller.items.add(testItem);
    }

    mergeNodes(testItem, node);

    controller.items.forEach((child) => {
      if (!nodes.some((n) => n.id === child.id)) {
        testItem.children.delete(child.id);
      }
    });
  }
}
