import { Logger } from "@shared";
import fastify from "fastify";

const FILE_NAME = "server/index.ts";

export const server = async function (props: {
  logger: Logger;
  port?: number;
}) {
  const { logger, port } = props;
  const app = fastify();

  app.get("/", async (req, res) => {
    const tagged = logger.tag(FILE_NAME, "/");
    tagged.log(() => ({
      message: ["Request", req],
    }));

    tagged.log(() => ({
      message: ["Result", res],
    }));

    return {
      message: "Hello, World!",
    };
  });

  const tagged = logger.tag(FILE_NAME, "listen");
  try {
    await app.listen({
      port,
    });
  } catch (e) {
    tagged.error(() => ({
      message: "Fastify error",
      error: e,
    }));
  }
};
