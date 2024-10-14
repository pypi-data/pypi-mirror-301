import * as fs from "fs";
import matter from "gray-matter";

/**
 * Defines the metadata for an engineered prompt.
 */
export interface EngineeredPromptMetadata {
  tests: {
    [key: string]: unknown;
  };
  test_path: string;
  [key: string]: unknown;
}

/**
 * Defines the basic structure for an engineered prompt specification.
 */
export interface EngineeredPromptSpecification {
  metadata: EngineeredPromptMetadata;
  input: string;
}

/**
 * Defines a profile for a test run.
 */
export interface TestProfile {
  version: string;
  include: TestProfileInclude[];
}

/**
 * Defines a reference to a prompt file to include in the test profile.
 * Can optionally refer to test identifiers from the file to include.
 */
export interface TestProfileInclude {
  filename: string;
  tests?: TestSpecificationInclude[];
}

/**
 * Defines a test specification within a test profile.
 */
export interface TestSpecificationInclude {
  id: string;
  samples: string[];
}

/**
 *
 * @param content The raw content to parse into an engineered prompt specification
 * @returns Returns the engineered prompt specification.
 */
export function parsePromptFileContent(
  content: string
): EngineeredPromptSpecification {
  const promptFileContent = matter(content);

  return {
    input: promptFileContent.content,
    metadata: promptFileContent.data as EngineeredPromptMetadata,
  };
}

/**
 * Parse a prompt file for a prompt specification.
 * @param filename The filename for the prompt file.
 */
export function parsePromptFile(
  filename: string
): Promise<EngineeredPromptSpecification> {
  return new Promise<EngineeredPromptSpecification>((resolve, reject) => {
    fs.readFile(filename, "utf8", (err, data) => {
      if (err) {
        reject(err);
      } else {
        const promptFileContent = matter(data);

        resolve({
          input: promptFileContent.content,
          metadata: promptFileContent.data as EngineeredPromptMetadata,
        });
      }
    });
  });
}

/**
 * Save the test profile to disk.
 * @param profile The test profile to save
 * @param filename The filename of the test profile
 * @returns Returns a resolved promise when the profile is saved.
 */
export function saveTestProfile(
  profile: TestProfile,
  filename: string
): Promise<void> {
  return new Promise<void>((resolve, reject) => {
    fs.writeFile(filename, JSON.stringify(profile, null, 4), "utf8", (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}
