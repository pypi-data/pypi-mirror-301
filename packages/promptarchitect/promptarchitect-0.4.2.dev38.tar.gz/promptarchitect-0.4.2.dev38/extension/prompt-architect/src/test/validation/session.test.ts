import * as vscode from 'vscode';
import * as assert from 'assert';
import { collectPromptFiles } from "../../validation/discovery";
import { mergeNodeTree } from '../../validation/session';

suite('session suite', () => {
    test('merge node tree', async () => {
        const controller = vscode.tests.createTestController('promptarchitect.testController', 'Test Controller');
        const nodeTree = await collectPromptFiles();

        mergeNodeTree(controller, nodeTree);

        // We're not testing all the nodes, but these ones should be present.

        assert.notEqual(controller.items.get("mixed-files-dir"), undefined, "directory not found");
        assert.notEqual(controller.items.get("mixed-files-dir")?.children.get("mixed-files-dir/file1.prompt"), undefined, "prompt file not found");
    });
});
